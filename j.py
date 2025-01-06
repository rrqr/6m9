import os
import re
import uuid
import time
from requests import Session
from rich.console import Console

# ألوان المخرجات
COLORS = {
    "magenta": "\033[1m\033[35m",
    "cyan": "\033[1m\033[36m",
    "green": "\033[1m\033[32m",
    "red": "\033[1m\033[31m",
    "reset": "\033[0m",
}

console = Console()
uid = str(uuid.uuid4())

def install_package(package_name):
    """تثبيت المكتبة إذا لم تكن موجودة."""
    try:
        __import__(package_name)
    except ImportError:
        os.system(f"pip install {package_name}")

# التأكد من تثبيت المكتبات المطلوبة
install_package("requests")
install_package("rich")

def header():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
{COLORS['magenta']} 
 ░▒▓██████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░  
{COLORS['cyan']}Bot Spam coded by @Abu6ms
Bot Instagram ~ 6m9.c
{COLORS['reset']}
    """)

def login_to_instagram(username, password):
    """محاولة تسجيل الدخول إلى Instagram"""
    with Session() as session:
        # Headers محدثة
        headers = {
            "User-Agent": "Instagram 123.0.0.21.114 Android (30/3.0; 320dpi; 720x1280; Xiaomi; Redmi Note 8; ginkgo; qcom; en_US)",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }

        data = {
            "_uuid": uid,
            "username": username,
            "password": password,
            "device_id": uid,
            "login_attempt_count": "0"
        }

        try:
            # إرسال طلب تسجيل الدخول
            response = session.post(
                "https://i.instagram.com/api/v1/accounts/login/",
                headers=headers,
                data=data
            )

            if "logged_in_user" in response.text:
                console.print("[+] Login Successful!", style="bold green")
                sessionid = response.cookies.get("sessionid")
                csrftoken = response.cookies.get("csrftoken")
                return sessionid, csrftoken
            elif "two_factor_required" in response.text:
                console.print("[!] Two-Factor Authentication required.", style="bold orange3")
            elif "challenge_required" in response.text:
                console.print("[!] Challenge Required. Please resolve security check.", style="bold red")
            elif "The password you entered is incorrect" in response.text:
                console.print("[!] Incorrect password. Please check and try again.", style="bold red")
            else:
                console.print(f"[!] Login failed: {response.json()}", style="bold red")
        except Exception as e:
            console.print(f"[!] Error during login: {e}", style="bold red")

        return None, None

def fetch_target_id(target, csrftoken):
    """محاولة الحصول على ID الهدف مع دعم إعادة المحاولة."""
    retries = 5  # عدد المحاولات
    for attempt in range(retries):
        try:
            response = get(
                f"https://www.instagram.com/{target}/?__a=1",
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'cookie': f'csrftoken={csrftoken}'
                }
            )

            if response.status_code == 200:
                target_data = response.json()
                return target_data['graphql']['user']['id']
            elif response.status_code == 429:
                console.print(f"[!] Rate limit reached. Retrying in {2 ** attempt} seconds...", style="bold yellow")
                time.sleep(2 ** attempt)  # تأخير باستخدام الأسلوب الأسي
            else:
                console.print(f"[!] Failed to fetch target ID. Status: {response.status_code}", style="bold red")
                break
        except Exception as e:
            console.print(f"[!] Error fetching target ID: {e}", style="bold red")
    return None

def report_instagram(target_id, sessionid, csrftoken):
    """الإبلاغ عن هدف معين."""
    report_types = [
        "Spam", "Self", "Sale", "Nudity", "Violence",
        "Hate Speech", "Harassment", "Instagram Issue",
        "Instagram Business", "Copyright", "Impression 3 Business",
        "Impression 3 Instagram", "Impression 4 Business", "Impression 4 Instagram",
        "Violence 1"
    ]

    console.print("\n".join([f"{idx + 1}. {r}" for idx, r in enumerate(report_types)]), style="bold cyan")
    report_type = input("[+] Enter Report Type Number: ")

    try:
        response = post(
            f"https://i.instagram.com/users/{target_id}/flag/",
            headers={
                "User-Agent": "Mozilla/5.0",
                "cookie": f"sessionid={sessionid}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            data=f"reason_id={report_type}&source_name=",
        )
        if response.status_code == 200:
            console.print("[+] Report Sent Successfully!", style="bold green")
        else:
            console.print(f"[!] Failed to report. Status: {response.status_code}", style="bold red")
    except Exception as e:
        console.print(f"[!] Error during report: {e}", style="bold red")

def starter():
    header()
    username = input("[+] Enter Instagram Username: ")
    password = input("[+] Enter Instagram Password: ")

    sessionid, csrftoken = login_to_instagram(username, password)

    if sessionid and csrftoken:
        target = input("[+] Enter Target Username: ")
        target_id = fetch_target_id(target, csrftoken)
        if target_id:
            report_instagram(target_id, sessionid, csrftoken)
        else:
            console.print("[!] Failed to fetch target ID.", style="bold red")

starter()
