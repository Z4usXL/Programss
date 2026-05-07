import requests
from SignerPy import sign, get
import time
import random
import os
import uuid
import binascii
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HiddenPrints:
    def __enter__(hex1):
        hex1._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(hex1, hex2, hex3, hex4):
        sys.stdout.close()
        sys.stdout = hex1._original_stdout

class SessionManager:
    
    def __init__(hex1, hex2):
        hex1.sessionid = hex2
        hex1.session = requests.Session()
        hex1.cdid = str(uuid.uuid4())
        hex1.openudid = str(binascii.hexlify(os.urandom(8)).decode())
        hex1.iid = str(random.randint(1, 10 ** 19))
        hex1.device_id = str(random.randint(1, 10 ** 19))
        hex1.pns_event_id_upload = str(uuid.uuid4())
        hex1.pns_event_id_commit = str(uuid.uuid4())
        hex1.x_tt_token = None
        hex1.cookies = None
        hex1.uid = None
        hex1.ticket_guard_public_key = None
        hex1.host = "api16-normal-c-alisg.tiktokv.com"
        
    def get_base_params(hex1):
        return {
            'manifest_version_code': '2023509040',
            '_rticket': str(int(time.time() * 1000)),
            'app_language': 'en',
            'app_type': 'normal',
            'iid': hex1.iid,
            'channel': 'googleplay',
            'device_type': 'SM-G935F',
            'language': 'en',
            'host_abi': 'arm64-v8a',
            'locale': 'en',
            'resolution': '576*1024',
            'openudid': hex1.openudid,
            'update_version_code': '2023509040',
            'is_pad': '0',
            'ac2': 'wifi',
            'cdid': hex1.cdid,
            'sys_region': 'US',
            'os_api': '25',
            'uoo': '0',
            'last_install_time': str(int(time.time()) - 1000),
            'timezone_name': 'Asia/Baghdad',
            'dpi': '191',
            'carrier_region': 'IQ',
            'ac': 'wifi',
            'device_id': hex1.device_id,
            'os': 'android',
            'mcc_mnc': '41845',
            'os_version': '7.1.2',
            'timezone_offset': '10800',
            'version_code': '350904',
            'app_name': 'musical_ly',
            'ab_version': '35.9.4',
            'version_name': '35.9.4',
            'device_brand': 'samsung',
            'op_region': 'IQ',
            'ssmix': 'a',
            'device_platform': 'android',
            'build_number': '35.9.4',
            'region': 'US',
            'aid': '1233',
            'ts': str(int(time.time())),
            'passport-sdk-version': '6021290',
        }
    
    def get_base_headers(hex1):
        hex2 = {
            'Host': hex1.host,
            'Connection': 'keep-alive',
            'passport-sdk-version': '6021290',
            'x-vc-bdturing-sdk-version': '2.3.8.i18n',
            'sdk-version': '2',
            'User-Agent': 'com.zhiliaoapp.musically/2023509040 (Linux; U; Android 7.1.2; en_US; SM-G935F; Build/N2G48H;tt-ok/3.12.13.4-tiktok)',
        }
        if hex1.x_tt_token:
            hex2['x-tt-token'] = hex1.x_tt_token
        return hex2
    
    def fetch_session_data(hex1):
        hex2 = hex1.get_base_params()
        hex2 = get(params=hex2)
        hex1.iid = hex2.get('iid', hex1.iid)
        hex1.device_id = hex2.get('device_id', hex1.device_id)
        hex1.cdid = hex2.get('cdid', hex1.cdid)
        hex1.openudid = hex2.get('openudid', hex1.openudid)
        hex1.cookies = {
            'sessionid': hex1.sessionid,
            'sessionid_ss': hex1.sessionid,
            'sid_tt': hex1.sessionid,
        }
        hex3 = hex1.get_base_headers()
        hex3['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        hex3['passport-sdk-settings'] = 'x-tt-token'
        hex3['passport-sdk-sign'] = 'x-tt-token'
        hex4 = sign(params=hex2, payload=None, version=4404)
        hex3.update(hex4)
        hex5 = f'https://{hex1.host}/passport/account/info/v2/'
        try:
            hex6 = hex1.session.get(
                hex5,
                params=hex2,
                headers=hex3,
                cookies=hex1.cookies,
                verify=False
            )
            if 'x-tt-token' in hex6.headers:
                hex1.x_tt_token = hex6.headers['x-tt-token']
            if hex6.status_code == 200:
                hex7 = hex6.json()
                if hex7.get('message') == 'success' or hex7.get('data'):
                    hex8 = hex7.get('data', {})
                    hex1.uid = str(hex8.get('user_id', hex8.get('uid', '')))
                    if not hex1.uid:
                        hex1.uid = str(hex8.get('user_id_str', ''))
                    hex1._extract_cookies(hex6)
                    hex1._fetch_public_key()
                    return True
                else:
                    return hex1._fetch_user_profile()
            else:
                return False
        except Exception as hex9:
            return False
    
    def _fetch_user_profile(hex1):
        hex2 = hex1.get_base_params()
        hex2 = get(params=hex2)
        hex3 = hex1.get_base_headers()
        hex4 = sign(params=hex2, payload=None, version=4404)
        hex3.update(hex4)
        hex5 = f'https://{hex1.host}/aweme/v1/user/profile/self/'
        try:
            hex6 = hex1.session.get(
                hex5,
                params=hex2,
                headers=hex3,
                cookies=hex1.cookies,
                verify=False
            )
            if 'x-tt-token' in hex6.headers:
                hex1.x_tt_token = hex6.headers['x-tt-token']
            if hex6.status_code == 200:
                hex7 = hex6.json()
                if hex7.get('status_code') == 0:
                    hex8 = hex7.get('user', {})
                    hex1.uid = str(hex8.get('uid', ''))
                    hex1._extract_cookies(hex6)
                    hex1._fetch_public_key()
                    return True
            return False
        except Exception as hex9:
            return False
    
    def _extract_cookies(hex1, hex2):
        for hex3 in hex2.cookies:
            hex1.cookies[hex3.name] = hex3.value
        hex1.cookies['sessionid'] = hex1.sessionid
        hex1.cookies['sessionid_ss'] = hex1.sessionid
        hex1.cookies['sid_tt'] = hex1.sessionid
        if 'odin_tt' not in hex1.cookies:
            hex1.cookies['odin_tt'] = binascii.hexlify(os.urandom(64)).decode()
        if 'passport_csrf_token' not in hex1.cookies:
            hex4 = binascii.hexlify(os.urandom(16)).decode()
            hex1.cookies['passport_csrf_token'] = hex4
            hex1.cookies['passport_csrf_token_default'] = hex4
        hex1.cookies['store-idc'] = 'alisg'
        hex1.cookies['store-country-code'] = 'iq'
    
    def _fetch_public_key(hex1):
        try:
            hex2 = hex1.get_base_params()
            hex2 = get(params=hex2)
            hex3 = hex1.get_base_headers()
            hex4 = sign(params=hex2, payload=None, version=4404)
            hex3.update(hex4)
            hex5 = f'https://{hex1.host}/passport/ticket/grant/'
            hex6 = hex1.session.post(
                hex5,
                params=hex2,
                headers=hex3,
                cookies=hex1.cookies,
                verify=False
            )
            if hex6.status_code == 200:
                hex7 = hex6.json()
                if isinstance(hex7, dict) and 'data' in hex7:
                    if isinstance(hex7['data'], dict) and 'public_key' in hex7['data']:
                        hex1.ticket_guard_public_key = hex7['data']['public_key']
        except Exception as hex8:
            pass
    
    def get_session_info(hex1):
        return {
            'uid': hex1.uid,
            'sessionid': hex1.sessionid,
            'device_id': hex1.device_id,
            'iid': hex1.iid,
            'cdid': hex1.cdid,
            'openudid': hex1.openudid,
            'x_tt_token': hex1.x_tt_token,
            'pns_event_id_upload': hex1.pns_event_id_upload,
            'pns_event_id_commit': hex1.pns_event_id_commit,
            'ticket_guard_public_key': hex1.ticket_guard_public_key,
            'cookies': hex1.cookies,
        }

hex1 = input("session : ").strip()
hex2 = input("imag : ").strip()

if not hex1:
    exit()

hex22 = os.path.dirname(os.path.abspath(__file__))
hex2 = os.path.join(hex22, hex2)

with HiddenPrints():
    hex3 = SessionManager(hex1)
    if not hex3.fetch_session_data():
        exit()
    hex4 = hex3.get_session_info()

try:
    with open(hex2, 'rb') as hex5:
        hex6 = hex5.read()
except FileNotFoundError:
    exit()

with HiddenPrints():
    hex7 = hex3.get_base_params()
    hex7['uid'] = hex4['uid']
    hex7 = get(params=hex7)
    hex8 = sign(params=hex7, payload=None, version=4404)
    hex9 = hex3.get_base_headers()
    hex9.update(hex8)
    hex9['X-Metasec-Pns-Event-Id'] = hex4['pns_event_id_upload']
    if hex4['x_tt_token']:
        hex9['x-tt-token'] = hex4['x_tt_token']
    hex10 = {
        'source': (None, '0'),
        'retry_type': (None, 'no_retry'),
        'file': ('profileHeaderCrop.png', hex6, 'application/octet-stream'),
    }
    hex11 = f'https://{hex3.host}/aweme/v1/upload/image/'
    hex12 = requests.post(
        hex11,
        params=hex7,
        cookies=hex4['cookies'],
        headers=hex9,
        files=hex10,
        verify=False,
    )

try:
    hex13 = hex12.json()
    hex14 = hex13.get('data', {}).get('uri', '')
    if not hex14:
        exit()
except Exception as hex15:
    exit()

with HiddenPrints():
    hex16 = hex3.get_base_params()
    hex16['uid'] = hex4['uid']
    hex16 = get(params=hex16)
    hex17 = {
        'uid': hex4['uid'],
        'page_from': '7',
        'school_type': '0',
        'avatar_source': '1',
        'avatar_uri': hex14,
    }
    hex18 = sign(params=hex16, payload=hex17, version=4404)
    hex19 = hex3.get_base_headers()
    hex19.update(hex18)
    hex19['X-Metasec-Pns-Event-Id'] = hex4['pns_event_id_commit']
    hex19['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    if hex4['ticket_guard_public_key']:
        hex19['Tt-Ticket-Guard-Public-Key'] = hex4['ticket_guard_public_key']
        hex19['Tt-Ticket-Guard-Iteration-Version'] = '0'
        hex19['Tt-Ticket-Guard-Version'] = '3'
    if hex4['x_tt_token']:
        hex19['x-tt-token'] = hex4['x_tt_token']
    hex20 = f'https://{hex3.host}/aweme/v1/commit/user/'
    hex21 = requests.post(
        hex20,
        params=hex16,
        cookies=hex4['cookies'],
        headers=hex19,
        data=hex17,
        verify=False,
    )

print(hex21.text if hex21.text else "")