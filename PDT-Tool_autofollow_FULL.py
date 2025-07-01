# =============================
# TOOL AUTO FOLLOW TIKTOK - H-T
# Phiên bản Python hoàn chỉnh - ADB + MÀU SẮC + DỪNG TOOL
# =============================

import time
import os
import sys
from datetime import datetime
from threading import Event

# =====================
# Cấu hình chung
# =====================
TOOL_TAC_GIA = "PHẠM ĐỨC TOÀN"
AUTH_FILE = "auth.key"
LOG_FILE = "job_log.txt"
ZALO = "0384056391"
FACEBOOK = "https://www.facebook.com/pdtlevi1998/"

# =====================
# Cờ dừng tool
# =====================
stop_event = Event()

# =====================
# ANSI màu chữ
# =====================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# =====================
# Giả định API (bạn có thể thay thế thành thật sau)
# =====================
def get_tiktok_jobs(auth_token):
    return [{
        "job_id": f"TIK{int(time.time()) % 100000}",
        "link": "https://www.tiktok.com/@example"
    }]

def confirm_job_done(job_id, auth_token):
    import requests
    url = "https://api.golike.net/api/job/complete"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    data = {
        "job_id": job_id
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            result = res.json()
            vn_reward = result.get("data", {}).get("reward", 0)  # tiền VNĐ
            return {"status": "success", "money": vn_reward}
        else:
            return {"status": "fail", "money": 0}
    except Exception as e:
        print("❌ Lỗi xác nhận job:", e)
        return {"status": "fail", "money": 0}

def get_linked_tiktok_id(auth_token):
    return f"tiktok_user_{int(time.time()) % 10}"

# =====================
# Chức năng chung
# =====================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""
{CYAN}╔════════════════════════════════════════════════════════════════════════════╗
║                         {YELLOW}TOOL AUTO FOLLOW TIKTOK{CYAN}                            ║
║                       {GREEN}Tác giả: {TOOL_TAC_GIA:<44}{CYAN}║
╠════════════════════════════════════════════════════════════════════════════╣
║ 📞 {YELLOW}Zalo    : {ZALO:<62}{CYAN}║
║ 🌐 {YELLOW}Facebook: {FACEBOOK:<62}{CYAN}║
╚════════════════════════════════════════════════════════════════════════════╝{RESET}
""")

def read_auth():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'r') as f:
            return f.read().strip()
    return None

def write_auth(token):
    with open(AUTH_FILE, 'w') as f:
        f.write(token.strip())

def log_job(job_id, coin, acc, duration):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    line = f"[{now}] ✅ Job ID: {job_id} | Coin: +{coin} | Time: {duration:.1f}s | Acc: {acc}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(line)

def adb_auto_follow():
    print("📲 Đang gửi lệnh ADB để nhấn Follow trên TikTok...")
    follow_x = 950
    follow_y = 500
    back_delay = 3

    os.system(f"adb shell input tap {follow_x} {follow_y}")
    time.sleep(back_delay)
    os.system("adb shell input keyevent 4")

# =====================
# Tool chính
# =====================
def run_job_mode(auto_follow=True, total_jobs=5, delay=6):
    import requests
    auth = read_auth()
    if not auth:
        print(RED + "❌ Chưa có mã Authorization. Vui lòng nhập lại." + RESET)
        return

    def get_pending_money():
        try:
            res = requests.get("https://api.golike.net/api/user/info", headers={"Authorization": f"Bearer {auth}"})
            if res.status_code == 200:
                return res.json().get("data", {}).get("pending_money", 0)
        except:
            pass
        return 0

    clear()
    banner()
    acc = get_linked_tiktok_id(auth)
    print(f"🔐 Mã Authorization: {auth}")
    print(f"📱 TikTok ID đã liên kết: {acc}\\n")
    print(f"⚙️ Đang chạy {total_jobs} job | Delay mỗi job: {delay} giây")
    print(f"{YELLOW}⛔ Nhấn Ctrl+C để dừng tool bất kỳ lúc nào...{RESET}")

    try:
        for i in range(1, total_jobs + 1):
            if stop_event.is_set():
                print(RED + "🚫 Tool đã dừng theo yêu cầu người dùng." + RESET)
                break

            print(f"\n🔄 Đang thực hiện job {i}/{total_jobs}...")
            job = get_tiktok_jobs(auth)[0]

            print(f"🌐 Mở TikTok: {job['link']}")
            os.system("adb shell am start -n com.zhiliaoapp.musically/com.ss.android.ugc.aweme.main.MainActivity")

            print(f"🕒 Đếm ngược {delay} giây...")
            for remaining in range(delay, 0, -1):
                if stop_event.is_set():
                    break
                sys.stdout.write(f"\r⏳ Còn lại: {remaining} giây   ")
                sys.stdout.flush()
                time.sleep(1)
            print("\r✅ Hết thời gian\n")

            if auto_follow:
                adb_auto_follow()

           try:
    res = confirm_job_done(job['job_id'], auth)
    if res['status'] == "success":
        money = res.get("money", 0)
        pending = get_pending_money(auth)
        print(GREEN + f"✅ Hoàn thành job {job['job_id']} | +{money} VNĐ | 💰 Chờ duyệt: {pending} VNĐ" + RESET)
        log_job(job['job_id'], f"{money} VNĐ", acc, delay)
    else:
        print(RED + f"❌ Lỗi khi xác nhận job {job['job_id']}" + RESET)

except Exception as e:
    print(RED + f"❌ Lỗi xử lý job {job['job_id']}: {e}" + RESET)

        print("\n🎉 Đã hoàn thành tất cả job!")

    except KeyboardInterrupt:
        stop_event.set()
        print(RED + "\n⛔ Tool đã được dừng bởi người dùng." + RESET)

# =====================
# Menu người dùng
# =====================
def main_menu():
    while True:
        clear()
        banner()
        print("[1] Vào Tool")
        print("[2] Nhập / thay đổi Mã Authorization")
        print("[9] Cập nhật tool từ GitHub")
        print("[0] Thoát")
        choice = input("\nNhập lựa chọn: ").strip()

        if choice == "1":
            sub_menu()
        elif choice == "2":
            new_auth = input("Nhập mã Authorization mới: ")
            write_auth(new_auth)
            print(GREEN + "✅ Đã lưu mã mới!" + RESET)
            input("Nhấn Enter để quay lại...")
        elif choice == "9":
            update_tool()
            input("Nhấn Enter để quay lại...")
        elif choice == "0":
            print("👋 Tạm biệt!")
            break
        else:
            print(RED + "❌ Lựa chọn không hợp lệ!" + RESET)
            time.sleep(1)

def update_tool():
    print("🔁 Đang cập nhật tool từ GitHub...")
    result = os.system("git pull")
    if result == 0:
        print(GREEN + "✅ Cập nhật thành công! Bạn đang dùng bản mới nhất." + RESET)
    else:
        print(RED + "❌ Cập nhật thất bại! Kiểm tra kết nối hoặc git chưa được cài." + RESET)

def sub_menu():
    while True:
        clear()
        banner()
        print("[1] Tự động Follow + tự đổi acc")
        print("[2] Follow thủ công + tự đổi acc")
        print("[0] Quay lại")
        choice = input("\nChọn chế độ: ").strip()

        if choice == "1":
            total = int(input("Nhập số job cần thực hiện: "))
            run_job_mode(auto_follow=True, total_jobs=total, delay=6)
            input("Nhấn Enter để quay lại...")
        elif choice == "2":
            total = int(input("Nhập số job cần thực hiện: "))
            delay = int(input("Thời gian đợi mỗi job (giây): "))
            run_job_mode(auto_follow=False, total_jobs=total, delay=delay)
            input("Nhấn Enter để quay lại...")
        elif choice == "0":
            break
        else:
            print(RED + "❌ Lựa chọn không hợp lệ!" + RESET)
            time.sleep(1)

# =====================
# Start tool
# =====================
if __name__ == "__main__":
    main_menu()
