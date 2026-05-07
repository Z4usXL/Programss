import time
import string
import secrets
import requests
import datetime
import random
import json
import uuid
import SignerPy
import binascii
from os import urandom
import requests, re, os, urllib.parse, random, binascii, uuid, time, secrets, string, json
from MedoSigner import Argus, Gorgon, Ladon, md5
import telebot

def xor(string):
    return "".join([hex(ord(c) ^ 5)[2:] for c in string])

def info(username):
    try:
        headers = {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Android 10; Pixel 3 Build/QKQ1.200308.002; wv) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                "Chrome/125.0.6394.70 Mobile Safari/537.36"
            )
        }

        html = requests.get(
            f"https://www.tiktok.com/@{username}",
            headers=headers,
            timeout=10
        ).text

        match = re.search(
            r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>',
            html
        )
        
        if not match:
            print("Hesap bulunamadı veya HTML yapısı değişti")
            return None
            
        data = json.loads(match.group(1))

        user = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
        stats = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["stats"]

        return {
            "id": user["id"],
            "username": user["uniqueId"],
            "name": user["nickname"],
            "verified": user["verified"],
            "private": user["privateAccount"],
            "create_time": time.strftime(
                "%Y-%m-%d",
                time.localtime(user["createTime"])
            ),
            "videos": stats["videoCount"],
            "followers": stats["followerCount"],
            "following": stats["followingCount"],
            "likes": stats["heartCount"],
        }

    except Exception as e:
        print(f"Info fonksiyonunda hata: {e}")
        return None

def check_tiktok_account(user):
    try:
        ts = str(int(time.time()))
        r = str(int(time.time() * 1000))
        mix_mode = "1"
        
        iid=random.randint(10**18,10**19-1); did=random.randint(10**18,10**19-1); dtype=random.choice(["M2102J20SG","SM-G998B","2201116SG","CPH2239","V2041"]); brand=random.choice(["POCO","Samsung","Xiaomi","OPPO","Vivo"]); odid=''.join(random.choices('0123456789abcdef',k=16)); cdid=str(uuid.uuid4())
        country="tr"
        os_version = f"{random.randint(7, 33)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
        url = "https://api16-normal-c-alisg.tiktokv.com/passport/find_account/tiktok_username/"
        username = xor(user)

        payload = {
            "mix_mode": mix_mode,
            "username": username
        }

        params = {
            "_rticket": r,
            "ab_version": "37.8.5",
            "ac": "WIFI",
            "ac2": "wifi",
            "aid": "1233",
            "app_language": country,
            "app_name": "musical_ly",
            "app_type": "normal",
            "build_number": "37.8.5",
            "carrier_region": country.upper(),
            "carrier_region_v2": "460",
            "cdid": cdid,
            "channel": "googleplay",
            "cronet_version": "75b93580_2024-11-28",
            "device_brand": brand,
            "device_id": did,
            "device_platform": "android",
            "device_type": dtype,
            "dpi": "320",
            "fixed_mix_mode": "1",
            "host_abi": "arm64-v8a",
            "iid": iid,
            "is_pad": "0",
            "language": country,
            "last_install_time": "1745162892",
            "locale": country,
            "manifest_version_code": "2023708050",
            "mix_mode": "1",
            "op_region": country.upper(),
            "openudid": odid,
            "os": "android",
            "os_api": "29",
            "os_version": os_version,
            "region": country.upper(),
            "request_tag_from": "h5",
            "resolution": "720%2A1280",
            "rrb": "%7B%7D",
            "scene": "4",
            "ssmix": "a",
            "support_webview": "1",
            "sys_region": country.upper(),
            "timezone_name": "Europe%2FIstanbul",
            "timezone_offset": "3600",
            "ts": ts,
            "ttnet_version": "4.2.210.6-tiktok",
            "uoo": "0",
            "update_version_code": "2023708050",
            "use_store_region_cookie": "1",
            "version_code": "370805",
            "version_name": "37.8.5",
            "app_version": "37.8.5"
        }

        m = SignerPy.sign(params=params, payload=payload)

        headers = {
            "User-Agent": (
                "com.zhiliaoapp.musically/370805 "
                "(Linux; U; Android 12; tr_TR; SO-51A; "
                "Build/58.2.B.0.520;tt-ok/3.12.13.21-ul)"
            )
        }
        headers.update(m)
        response = requests.post(url, params=params, data=payload, headers=headers, timeout=10)
        
        token = None
        try:
            data = response.json()
            token = data.get("data", {}).get("token")
        except:
            print("Token alınamadı veya API yanıtı geçersiz")
            return "❌ Hesap bulunamadı veya API hatası oluştu."
            
        if not token:
            return "❌ Hesap bulunamadı veya kullanıcı adı geçersiz."
            
        ur = "https://api16-normal-c-alisg.ttapis.com/passport/auth/available_ways/"
        params.update({"not_login_ticket": token})
        m2 = SignerPy.sign(params=params, payload=payload)
        
        hea = {
            "User-Agent": (
                "com.zhiliaoapp.musically/370805 "
                "(Linux; U; Android 12; tr_TR; SO-51A; "
                "Build/58.2.B.0.520;tt-ok/3.12.13.21-ul)"
            )
        }
        hea.update(m2)
        
        mxy = info(user)
        if not mxy:
            return "❌ Hesap bilgileri alınamadı. Kullanıcı adını kontrol edin."
            
        response2 = requests.post(ur, params=params, headers=hea, data=payload, timeout=10)
        
        try:
            response_data = response2.json()
            data_info = response_data.get("data", {})
            
            # platform değişkenini güvenli şekilde al
            platform_data = data_info.get("oauth_platforms", [])
            if isinstance(platform_data, list):
                platform = platform_data
            else:
                platform = []
                
            email = data_info.get("has_email", False)
            phone = data_info.get("has_mobile", False)
            oauth = data_info.get("has_oauth", False)
            passkey = data_info.get("has_passkey", False)
            password = data_info.get("has_pwd", False)
            
        except Exception as e:
            print(f"API yanıtı işlenirken hata: {e}")
            # Varsayılan değerler
            platform = []
            email = False
            phone = False
            oauth = False
            passkey = False
            password = False
            
        name = mxy.get("name", "Bilinmiyor")
        verify = "✅" if mxy.get("verified") else "❌"
        private = "✅" if mxy.get("private") else "❌"
        create_time = mxy.get("create_time", "Bilinmiyor")
        video = mxy.get("videos", 0)
        foll = mxy.get("followers", 0)
        follow = mxy.get("following", 0)
        like = mxy.get("likes", 0)
        username_display = mxy.get("username", user)
        
        # Platform kontrolü - güvenli şekilde
        platforms = "N/A"
        if platform and isinstance(platform, list):
            if "google" in platform:
                platforms = "Google"
            elif "facebook" in platform:
                platforms = "Facebook"
            elif "twitter" in platform:
                platforms = "Twitter"
            elif "apple" in platform:
                platforms = "Apple"
            else:
                platforms = ", ".join(platform) if platform else "N/A"

        email_status = "True" if email else "False"
        phone_status = "True" if phone else "False"
        oauth_status = "True" if oauth else "False"
        platform_status = f"True ({platforms})" if platforms != "N/A" else "False"
        passkey_status = "True" if passkey else "False"
        password_status = "True" if password else "False"

        ss = f"""
╔════════ ACCOUNT ════════╗    
║👤 Name     : {name}    
║🆔 User     : @{username_display}    
║✅ Verified : {verify}    
║🔒 Private  : {private}    
║📅 Created  : {create_time}    
╠════════ STATS ══════════╣    
║🎥 Videos   : {video}    
║👥 Followers: {foll}    
║➡️ Following: {follow}    
║❤️ Likes    : {like}    
╠════════ SECURITY ════════╣    
║📧 Email    : {email_status}    
║📱 Phone    : {phone_status}    
║🌐 OAuth    : {oauth_status}     
║🔑 Passkey  : {passkey_status}
║🔓 Password : {password_status}    
╠═══════════════════════╣    
║developer: @Z4usX
╚═══════════════════════╝    
"""
        return ss
        
    except Exception as e:
        print(f"Hata: {e}")
        return f"❌ Bir hata oluştu:\n{str(e)}"

print(check_tiktok_account("username"))