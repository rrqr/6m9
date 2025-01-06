import os
import re
import uuid
import time
from requests import post, get
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
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░    ░▒▓██▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████████▓▒░  ░▒▓██▓▒░  ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓██▓▒░    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  

{COLORS['cyan']}Bot Spam coded by @Abu6ms
Bot Instagram ~ 6m9.c
{COLORS['reset']}
    """)


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
    header()
    print(f"""
{COLORS['cyan']} _____________________________
| {COLORS['magenta']}~ Choose a report type       {COLORS['cyan']} |
|_____________________________|
""")
    report_types = [
        "Spam", "Self", "Sale", "Nudity", "Violence",
        "Hate Speech", "Harassment", "Instagram Issue",
        "Instagram Business", "Copyright", "Impression 3 Business",
        "Impression 3 Instagram", "Impression 4 Business", "Impression 4 Instagram",
        "Violence 1"
    ]

    for idx, report in enumerate(report_types, 1):
        print(f"| {COLORS['green']}{idx} ~ {COLORS['cyan']}{report}")

    try:
        report_type = int(input("\n-> Enter number (1-15): "))
        if not 1 <= report_type <= 15:
            console.print("Invalid choice! Try again.", style="bold red")
            return
    except ValueError:
        console.print("Invalid input. Please enter a number.", style="bold red")
        return

    while True:
        try:
            response = post(
                f"https://i.instagram.com/users/{target_id}/flag/",
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Host": "i.instagram.com",
                    "cookie": f"sessionid={sessionid}",
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
                data=f'source_name=&reason_id={report_type}&frx_context=',
                allow_redirects=False
            )
            if response.status_code == 429:
                console.print("[!] Rate limit exceeded. Try later.", style="bold red")
                break
            elif response.status_code == 500:
                console.print("[!] Target not found.", style="bold red")
                break
            else:
                console.print(f"Report sent successfully! Status: {response.status_code}", style="bold green")
        except Exception as e:
            console.print(f"[!] Error: {e}", style="bold red")
            break


def starter():
    """الدالة الرئيسية لتسجيل الدخول ومعالجة الهدف."""
    user = input(f"{COLORS['cyan']}[+] Username: {COLORS['reset']}@")
    if not user:
        console.print("[!] You must provide a username.", style="bold red")
        return

    password = input(f"{COLORS['cyan']}[+] Password: {COLORS['reset']}")
    if not password:
        console.print("[!] You must provide a password.", style="bold red")
        return

    try:
        # تسجيل الدخول
        login_response = post(
            'https://i.instagram.com/api/v1/accounts/login/',
            headers={
                'User-Agent': 'Instagram 114.0.0.38.120 Android (30/3.0; 216dpi; 1080x2340; huawei/google; Nexus 6P; angler; angler; en_US)',
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                'Host': 'i.instagram.com'
            },
            data={
                '_uuid': uid,
                'password': password,
                'username': user,
                'device_id': uid,
                'from_reg': 'false',
                '_csrftoken': 'missing',
                'login_attempt_count': '0'
            },
            allow_redirects=True
        )

        if 'logged_in_user' in login_response.text:
            console.print("- Login Successful!", style="bold green")
            sessionid = login_response.cookies.get('sessionid')
            csrftoken = login_response.cookies.get('csrftoken')

            # إدخال الهدف
            target = input("- Enter Target Username: ")
            if not target:
                console.print("[!] Target username is required.", style="bold red")
                return

            # الحصول على ID الهدف مع إعادة المحاولة
            target_id = fetch_target_id(target, csrftoken)
            if target_id:
                console.print(f"- Target ID: {target_id}", style="bold green")
                report_instagram(target_id, sessionid, csrftoken)
            else:
                console.print("[!] Failed to fetch target ID after multiple attempts.", style="bold red")
        else:
            console.print("[!] Login failed. Check credentials or try again later.", style="bold red")

    except Exception as e:
        console.print(f"[!] Error during login process: {e}", style="bold red")


header()
starter()
