import requests
import os
from colorama import Fore, Style, init

init(autoreset=True)

def prnt_upload():
    print(Fore.CYAN + "Enter image file path:")
    image_path = input(Fore.YELLOW + "➤ ")

    if not os.path.exists(image_path):
        print(Fore.RED + "❌ File not found!")
        return

    url = "https://prntscr.com/upload.php"

    files = {
        'image': open(image_path, 'rb')
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",
        'origin': "https://prnt.sc",
        'referer': "https://prnt.sc/"
    }

    print(Fore.BLUE + "📤 Uploading...")

    try:
        response = requests.post(url, files=files, headers=headers)
        data = response.json()

        if data["status"] == "success":
            link = data["data"]
            print(Fore.GREEN + "✅ Upload successful!")
            print(Fore.MAGENTA + "🔗 Image Link:")
            print(Style.BRIGHT + link)
        else:
            print(Fore.RED + "❌ Upload failed!")

    except Exception as e:
        print(Fore.RED + "❌ Error:", e)


prnt_upload()