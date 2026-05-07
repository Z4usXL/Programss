import requests
import random
from cfonts import say
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
say("SMSPARK", font="block", colors=["yellow", "cyan"], align="center")
say("LOGIN", font="block", colors=["cyan", "yellow"], align="center")
print(CYAN + "═" * 30 + RESET)
print(f"{YELLOW}Developer: @Z4usX{RESET}")
print(CYAN + "═" * 30 + RESET + "\n")
email = input(f"{CYAN}E-mail: {RESET}")
password = input(f"{CYAN}Şifre: {RESET}")
url = "https://smspark.net/ajax/login"
headers = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Linux; Android 12)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"]),
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://smspark.net/login"}
data = {"email": email,"password": password}
print(f"\n{YELLOW}🔄 Giriş deneniyor...{RESET}\n")
try:
    r = requests.post(url, headers=headers, data=data, timeout=15)
    print(f"{CYAN}📥 RAW RESPONSE:{RESET}")
    print(r.text)
    print()
    js = r.json()
    if js.get("success") is True:
        print(f"{GREEN}{BOLD}✅ LOGIN BAŞARILI{RESET}")
    elif js.get("success") is False:
        print(f"{RED}{BOLD}❌ LOGIN BAŞARISIZ{RESET}")
    else:
        print(f"{YELLOW}⚠️ Beklenmeyen yanıt:{RESET} {js}")
except Exception as e:
    print(f"{RED}❌ Hata oluştu: {e}{RESET}")