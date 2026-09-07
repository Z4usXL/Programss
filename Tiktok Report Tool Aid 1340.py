# -*- coding: utf-8 -*-

import requests
import json
import time
import random
import string
import uuid
import threading
import queue
import concurrent.futures
import os
import SignerPy

YESIL = "\033[92m"
KIRMIZI = "\033[91m"
SIFIRLA = "\033[0m"
SARI = "\033[93m"
MAVI = "\033[94m"
MOR = "\033[95m"

URL = "https://api16-normal-c-alisg.tiktokv.com/aweme/v2/aweme/feedback/"

HEDEF_OBJECT_ID = " target account ID"
HEDEF_OWNER_ID = " target account ID"


RAPOR_NEDENLERI = {
    "90086": "porn",
    "91015": " ",
    "9004": "",
    "90071": ""
}

# Format: "http://kullanici:sifre@host:port" veya "http://host:port"
PROXY_LISTESI = [
    "",

]

THREAD_SAYISI = 50
kilit = threading.Lock()
BASARILI_SAYAC = 0
BASARISIZ_SAYAC = 0

def proxy_dosyadan_yukle(dosya_adi="proxies.txt"):
    global PROXY_LISTESI
    if os.path.exists(dosya_adi):
        try:
            with open(dosya_adi, 'r') as f:
                dosya_proxyleri = [satir.strip() for satir in f if satir.strip() and not satir.startswith('#')]
                if dosya_proxyleri:
                    PROXY_LISTESI = dosya_proxyleri
                    print(f"{YESIL}[PROXY] {len(PROXY_LISTESI)} adet proxy dosyadan yüklendi.{SIFIRLA}")
                    return
        except Exception as e:
            print(f"{KIRMIZI}[PROXY] Dosyadan okunurken hata: {str(e)}{SIFIRLA}")
    
    print(f"{YESIL}[PROXY] Koddaki proxy listesi kullanılıyor ({len(PROXY_LISTESI)} adet).{SIFIRLA}")

def rastgele_proxy():
    if PROXY_LISTESI:
        proxy = random.choice(PROXY_LISTESI)
        if proxy.startswith("http://") or proxy.startswith("https://") or proxy.startswith("socks5://"):
            return {"http": proxy, "https": proxy}
        else:
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    return None

def rastgele_rapor_nedeni():
    return random.choice(list(RAPOR_NEDENLERI.keys()))

def rastgele_cihaz_uret():
    android_surumleri = ["10", "11", "12", "13", "14"]
    android_api = {"10": "29", "11": "30", "12": "31", "13": "33", "14": "34"}
    
    marka_modeller = {
        "POCO": ["M2102J20SG", "M2101K6G", "M2007J20CG", "M1901F7G", "M2012K11AG", "M2103K19G"],
        "Samsung": ["SM-G991B", "SM-A525F", "SM-G781B", "SM-A325F", "SM-G998B", "SM-A725F"],
        "Xiaomi": ["2107119DC", "2201116SG", "21081111RG", "2201117TY", "21061110AG", "2201122G"],
        "Huawei": ["ELS-NX9", "YAL-L21", "ANA-NX9", "JNY-LX1", "VOG-L29", "MAR-LX1A"],
        "OnePlus": ["LE2113", "IN2023", "AC2003", "HD1903", "GM1903", "KB2003"],
        "Oppo": ["CPH2211", "CPH2179", "CPH2207", "CPH2067", "CPH2269", "CPH2247"],
        "Vivo": ["V2040", "V2027", "V2019", "V2041", "V2050", "V2061"],
        "Realme": ["RMX3085", "RMX3063", "RMX2170", "RMX3081", "RMX3201", "RMX3261"],
        "Google": ["Pixel 5", "Pixel 6", "Pixel 4a", "Pixel 7", "Pixel 6a", "Pixel 8"],
        "Motorola": ["moto g60", "moto g50", "moto g100", "moto edge20", "moto g31", "moto g71"]
    }
    
    bolgeler = ["TR", "DE", "US", "UK", "FR", "ES", "IT", "NL", "RU", "BR", "CA", "AU"]
    diller = ["tr", "de", "en", "fr", "es", "it", "nl", "ru", "pt", "en-GB"]
    yerel_ayar = ["tr-TR", "de-DE", "en-US", "en-GB", "fr-FR", "es-ES", "it-IT", "nl-NL", "ru-RU", "pt-BR"]
    saat_dilimleri = ["Europe/Istanbul", "Europe/Berlin", "America/New_York", "Europe/London", "Europe/Paris", "Europe/Madrid", "Europe/Rome", "Europe/Amsterdam", "Europe/Moscow", "America/Sao_Paulo"]
    saat_farklari = {"Europe/Istanbul": "10800", "Europe/Berlin": "7200", "America/New_York": "-18000", "Europe/London": "0", "Europe/Paris": "3600", "Europe/Madrid": "3600", "Europe/Rome": "3600", "Europe/Amsterdam": "3600", "Europe/Moscow": "10800", "America/Sao_Paulo": "-10800"}
    
    marka = random.choice(list(marka_modeller.keys()))
    model = random.choice(marka_modeller[marka])
    android_surum = random.choice(android_surumleri)
    api_seviye = android_api[android_surum]
    bolge = random.choice(bolgeler)
    dil = random.choice(diller)
    yerel = random.choice(yerel_ayar)
    saat_dilimi = random.choice(saat_dilimleri)
    saat_farki = saat_farklari[saat_dilimi]
    
    cozunurlukler = ["720*1560", "1080*2274", "1080*2400", "1440*3120", "1080*2340", "720*1600", "1440*2560", "1080*2160"]
    cozunurluk = random.choice(cozunurlukler)
    
    dpi_degerleri = ["320", "352", "400", "420", "440", "480", "520", "560"]
    dpi = random.choice(dpi_degerleri)
    
    build_numarasi = f"{random.choice(['SKQ1', 'SP1A', 'TP1A', 'RQ3A', 'SQ3A', 'RP1A'])}.{''.join(random.choices(string.digits, k=6))}.{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"
    
    device_id = str(random.randint(7000000000000000000, 7999999999999999999))
    iid = str(random.randint(7000000000000000000, 7999999999999999999))
    openudid = ''.join(random.choices('0123456789abcdef', k=16))
    cdid = str(uuid.uuid4())
    
    x_tt_token = ''.join(random.choices('0123456789abcdef', k=64)) + "--" + ''.join(random.choices('0123456789abcdef', k=32))
    
    ag_tipi = random.choice(["wifi", "wifi5g", "4g", "5g"])
    ac_degeri = ag_tipi if ag_tipi != "5g" else "wifi5g"
    
    surum_kodu = "430245"
    surum_adi = "43.2.45"
    manifest_kodu = "430245"
    
    return {
        "device_id": device_id,
        "iid": iid,
        "openudid": openudid,
        "cdid": cdid,
        "marka": marka,
        "model": model,
        "android_surum": android_surum,
        "api_seviye": api_seviye,
        "bolge": bolge,
        "dil": dil,
        "yerel_ayar": yerel,
        "saat_dilimi": saat_dilimi,
        "saat_farki": saat_farki,
        "cozunurluk": cozunurluk,
        "dpi": dpi,
        "build_numarasi": build_numarasi,
        "ag_tipi": ag_tipi,
        "ac_degeri": ac_degeri,
        "surum_kodu": surum_kodu,
        "surum_adi": surum_adi,
        "manifest_kodu": manifest_kodu,
        "x_tt_token": x_tt_token
    }

def tek_rapor_gonder(rapor_no):
    global BASARILI_SAYAC, BASARISIZ_SAYAC
    
    try:
        cihaz = rastgele_cihaz_uret()
        anlik_ts = str(int(time.time() * 1000))
        
        rapor_nedeni = rastgele_rapor_nedeni()
        neden_aciklama = RAPOR_NEDENLERI[rapor_nedeni]
        
        user_agent = f"com.zhiliaoapp.musically.go/{cihaz['surum_kodu']} (Linux; U; Android {cihaz['android_surum']}; {cihaz['yerel_ayar']}; {cihaz['model']}; Build/{cihaz['build_numarasi']};tt-ok/3.12.13.50.lite-alpha.3-log)"
        
        params = {
            "hide_nav_bar": "1",
            "report_type": "user",
            "object_id": HEDEF_OBJECT_ID,
            "owner_id": HEDEF_OWNER_ID,
            "lang": cihaz["dil"],
            "click_start_time": str(int(time.time() * 1000) - random.randint(500, 2000)),
            "report_desc": "",
            "uri": "",
            "reason": rapor_nedeni,
            "category": "",
            "logout_reporter_email": "",
            "is_osa_report_cg": "false",
            "is_osa_report": "false",
            "request_tag_from": "h5",
            "_rticket": anlik_ts,
            "manifest_version_code": cihaz["manifest_kodu"],
            "app_language": cihaz["dil"],
            "app_type": "normal",
            "iid": cihaz["iid"],
            "app_package": "com.zhiliaoapp.musically.go",
            "channel": "googleplay",
            "device_type": cihaz["model"],
            "language": cihaz["dil"],
            "host_abi": random.choice(["arm64-v8a", "armeabi-v7a"]),
            "locale": cihaz["yerel_ayar"],
            "resolution": cihaz["cozunurluk"],
            "openudid": cihaz["openudid"],
            "update_version_code": cihaz["surum_kodu"],
            "ac2": cihaz["ac_degeri"],
            "cdid": cihaz["cdid"],
            "sys_region": cihaz["bolge"],
            "os_api": cihaz["api_seviye"],
            "timezone_name": cihaz["saat_dilimi"],
            "dpi": cihaz["dpi"],
            "carrier_region": cihaz["bolge"],
            "ac": cihaz["ag_tipi"],
            "os": "android",
            "device_id": cihaz["device_id"],
            "os_version": cihaz["android_surum"],
            "timezone_offset": cihaz["saat_farki"],
            "version_code": cihaz["surum_kodu"],
            "app_name": "musically_go",
            "ab_version": cihaz["surum_adi"],
            "version_name": cihaz["surum_adi"],
            "device_brand": cihaz["marka"],
            "op_region": cihaz["bolge"],
            "ssmix": "a",
            "device_platform": "android",
            "build_number": cihaz["surum_adi"],
            "region": cihaz["bolge"],
            "aid": "1340",
            "ts": anlik_ts
        }
        
        imzalar = SignerPy.sign(params=params, payload=None, aid=1340, version=8404)
        
        headers = {
            "User-Agent": user_agent,
            "rpc-persist-pyxis-policy-v-tnc": "1",
            "x-ss-dp": "1340",
            "x-tt-dataflow-id": "671088658",
            "sdk-version": "2",
            "x-tt-token": cihaz["x_tt_token"],
            "passport-sdk-version": "-1",
            "x-tt-ultra-lite": "1",
            "x-tt-request-tag": "n=0",
            "x-vc-bdturing-sdk-version": "2.3.15.i18n",
            "x-tt-store-region": cihaz["bolge"],
            "x-tt-store-region-src": "did",
            "ttzip-tlb": "1",
            "x-ladon": imzalar["x-ladon"],
            "x-khronos": imzalar["x-khronos"],
            "x-argus": imzalar["x-argus"],
            "x-gorgon": imzalar["x-gorgon"]
        }
        
        proxy = rastgele_proxy()
        
        if proxy:
            response = requests.get(URL, params=params, headers=headers, proxies=proxy, timeout=15)
        else:
            response = requests.get(URL, params=params, headers=headers, timeout=15)
        
        sonuc = response.json()
        
        with kilit:
            if sonuc.get("status_code") == 0:
                BASARILI_SAYAC += 1
                print(f"{YESIL}[BAŞARILI]{SIFIRLA} Rapor #{rapor_no} gönderildi. Neden: {neden_aciklama} ({rapor_nedeni})|{sonuc}")
            else:
                BASARISIZ_SAYAC += 1
                print(f"{KIRMIZI}[HATA]{SIFIRLA} Rapor #{rapor_no} başarısız. Neden: {neden_aciklama} ({rapor_nedeni}) Yanıt: {response.text[:100]}")
    
    except requests.exceptions.ProxyError:
        with kilit:
            BASARISIZ_SAYAC += 1
            print(f"{KIRMIZI}[PROXY HATASI]{SIFIRLA} Rapor #{rapor_no} proxy bağlantı hatası.")
    except requests.exceptions.Timeout:
        with kilit:
            BASARISIZ_SAYAC += 1
            print(f"{KIRMIZI}[ZAMAN AŞIMI]{SIFIRLA} Rapor #{rapor_no} zaman aşımına uğradı.")
    except requests.exceptions.ConnectionError:
        with kilit:
            BASARISIZ_SAYAC += 1
            print(f"{KIRMIZI}[BAĞLANTI HATASI]{SIFIRLA} Rapor #{rapor_no} bağlantı hatası.")
    except Exception as e:
        with kilit:
            BASARISIZ_SAYAC += 1
            print(f"{KIRMIZI}[İSTİSNA]{SIFIRLA} Rapor #{rapor_no} hata: {str(e)}")

def rapor_gonder_thread(rapor_adedi, thread_sayisi):
    global BASARILI_SAYAC, BASARISIZ_SAYAC
    
    BASARILI_SAYAC = 0
    BASARISIZ_SAYAC = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_sayisi) as executor:
        gorevler = [executor.submit(tek_rapor_gonder, i+1) for i in range(rapor_adedi)]
        concurrent.futures.wait(gorevler)
    
    return BASARILI_SAYAC, BASARISIZ_SAYAC

if __name__ == "__main__":
    print(f"{MAVI}══════════════════════════════════════════════════════════════{SIFIRLA}")
    print(f"{MAVI}         TikTok Toplu Raporlama Aracı v3.0{SIFIRLA}")
    print(f"{MAVI}══════════════════════════════════════════════════════════════{SIFIRLA}")

    proxy_dosyadan_yukle()
    
    try:
        thread_girdi = input(f"{SARI}Thread sayısı (varsayılan: 5): {SIFIRLA}").strip()
        if thread_girdi == "":
            thread_girdi = "5"
        THREAD_SAYISI = int(thread_girdi)
        if THREAD_SAYISI < 1:
            THREAD_SAYISI = 1
        elif THREAD_SAYISI > 50:
            THREAD_SAYISI = 50
            print(f"{SARI}Thread sayısı 50 ile sınırlandırıldı.{SIFIRLA}")
    except ValueError:
        THREAD_SAYISI = 5
        print(f"{SARI}Geçersiz değer. Varsayılan 5 thread kullanılacak.{SIFIRLA}")
    
    try:
        adet = int(input(f"{SARI}Kaç adet rapor gönderilsin: {SIFIRLA}"))
    except ValueError:
        adet = 10
        print(f"{SARI}Geçersiz değer. Varsayılan 10 rapor gönderilecek.{SIFIRLA}")
    
    print(f"\n{MAVI}══════════════════════════════════════════════════════════════{SIFIRLA}")
    print(f"{SARI}Raporlama başlıyor...{SIFIRLA}")
    print(f"{SARI}Toplam Rapor: {adet} | Thread: {THREAD_SAYISI} | Proxy: {len(PROXY_LISTESI)} adet{SIFIRLA}")
    print(f"{MAVI}══════════════════════════════════════════════════════════════{SIFIRLA}\n")
    
    baslangic = time.time()
    toplam_basarili, toplam_basarisiz = rapor_gonder_thread(adet, THREAD_SAYISI)
    bitis = time.time()
    
    sure = bitis - baslangic
    
    print(f"\n{MAVI}══════════════════════════════════════════════════════════════{SIFIRLA}")
    print(f"{YESIL}Toplam {toplam_basarili} başarılı rapor gönderildi.{SIFIRLA}")
    if toplam_basarisiz > 0:
        print(f"{KIRMIZI}Toplam {toplam_basarisiz} rapor başarısız oldu.{SIFIRLA}")
    print(f"{MOR}Toplam süre: {sure:.2f} saniye{SIFIRLA}")
    print(f"{MAVI}══════════════════════════════════════════════════════════════{SIFIRLA}")