import os
import time
import threading
import sys

# Color Codes (ANSI)
G = "\033[1;32m" # Green
R = "\033[1;31m" # Red
C = "\033[1;36m" # Cyan
Y = "\033[0;33m" # Yellow
W = "\033[0;37m" # White
RE = "\033[00m"  # Reset

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_tool(module, name):
    clear()
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RE}")
    print(f"{G} [🚀] INITIALIZING: {W}{name}{RE}")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RE}")
    
    if module.check_approval():
        try:
            # Background Monitoring Threads
            threading.Thread(target=module.background_key_verification, daemon=True).start()
            threading.Thread(target=module.session_refiller, daemon=True).start()
            threading.Thread(target=module.live_dashboard, daemon=True).start()
            
            # Heavy Task Worker Threads
            for _ in range(module.NUM_THREADS):
                threading.Thread(target=module.worker_thread, daemon=True).start()
            
            print(f"{G} [✓] {name} is now running...{RE}")
            print(f"{Y} [!] Press Ctrl+C to stop and return to menu.{RE}\n")
            
            while True: 
                time.sleep(1)
        except KeyboardInterrupt:
            module.stop_event.set()
            print(f"\n{R} [!] Stopping {name}... Please wait.{RE}")
            time.sleep(2)
            menu()

def menu():
    clear()
    # Banner Section
    print(f"{C}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{RE}")
    print(f"{C}┃{W}         ✨ STARLINK ULTIMATE SCANNER ✨        {C}┃{RE}")
    print(f"{C}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RE}")
    
    # Options Section
    print(f" {G}[01]{W}[•](0-9)&(a-z) (6 Digits){RE}")
    print(f" {G}[02]{W}[•](a-z) (6 Digits){RE}")
    print(f" {G}[03]{W}[•](0-9) (7 Digits){RE}")
    print(f" {G}[04]{W}[•](0-9) (6 Digits){RE}")
    print(f" {G}[05]{W}[•](0-9)&(z-z)&(A-Z) (6 Digits){RE}") 
    print(f" {R}[00]{R}[•]Exit System{RE}")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RE}")
    
    choice = input(f"{Y} ❯❯ Select Method: {RE}").strip()
    
    try:
        if choice in ['1', '01']:
            import engcode
            start_tool(engcode, "END&NUMBER (6D)")
        elif choice in ['2', '02']:
            import englow
            start_tool(englow, "ENG LOWERCASE (6D)")
        elif choice in ['3', '03']:
            import code7
            start_tool(code7, "NUMBER CODE (7D)")
        elif choice in ['4', '04']:
            import procode
            start_tool(procode, "NUMBER CODE (6D)")
        elif choice in ['5', '05']:
            import numengupandlow
            start_tool(numengupandlow, "NUM&ENG UPPER/LOWER (6D)")
        elif choice in ['0', '00']:
            print(f"\n{Y} [!] Exiting... THANKS FOR USING MY TOOL!{RE}")
            sys.exit()
        else:
            print(f"{R} [X] Invalid selection! Try again.{RE}")
            time.sleep(1.5)
            menu()
            
    except ImportError as e:
        module_name = str(e).split("'")[-2]
        print(f"\n{R} [Critical Error]: {W}Missing system file '{module_name}.so'{RE}")
        print(f"{Y} Please ensure all module files are in the same directory.{RE}")
        input(f"\n{W} Press [Enter] to return to menu...{RE}")
        menu()

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{R} [!] Forced Shutdown.{RE}")
        sys.exit()
        