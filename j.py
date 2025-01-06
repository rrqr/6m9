import os
import re
import uuid
from requests import post, get
from datetime import datetime
from rich.console import Console

# Colors for output
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
    """Install the package if not already installed."""
    try:
        __import__(package_name)
    except ImportError:
        os.system(f"pip install {package_name}")


# Ensure required packages are installed
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


def report_instagram(target_id, sessionid, csrftoken):
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
                console.print("Rate limit exceeded. Try later.", style="bold red")
                break
            elif response.status_code == 500:
                console.print("Target not found.", style="bold red")
                break
            else:
                console.print(f"Report sent successfully! Status: {response.status_code}", style="bold green")
        except Exception as e:
            console.print(f"Error: {e}", style="bold red")
            break


def starter():
    user = input(f"{COLORS['cyan']}[+] Username: {COLORS['reset']}@")
    password = input(f"{COLORS['cyan']}[+] Password: {COLORS['reset']}")
    # Add login and reporting flow here...


header()
starter()
