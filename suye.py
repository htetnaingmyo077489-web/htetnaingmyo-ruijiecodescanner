import os
import time
import threading
import sys

# Colors
bgreen = "\033[1;32m"
bred = "\033[1;31m"
bcyan = "\033[1;36m"
yellow = "\033[0;33m"
white = "\033[0;37m"
reset = "\033[00m"

def clear():
    os.system('clear')

def start_tool(module, name):
    clear()
    print(f"{bcyan}Starting {name}...{reset}")
    if module.check_approval():
        try:
            # Background Threads များစတင်ခြင်း
            threading.Thread(target=module.background_key_verification, daemon=True).start()
            threading.Thread(target=module.session_refiller, daemon=True).start()
            threading.Thread(target=module.live_dashboard, daemon=True).start()
            
            # Worker Threads များစတင်ခြင်း
            for _ in range(module.NUM_THREADS):
                threading.Thread(target=module.worker_thread, daemon=True).start()
            
            while True: 
                time.sleep(1)
        except KeyboardInterrupt:
            module.stop_event.set()
            print(f"\n{bred}Stopping {name}...{reset}")
            time.sleep(2)
            menu()

def menu():
    clear()
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    print(f"{white}         STARLINK ALL-IN-ONE SCANNER          {reset}")
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    print(f"{bgreen}[1]{reset} Eng Mixed (Original - 50 Threads)")
    print(f"{bgreen}[2]{reset} Eng Lowercase (150 Threads)")
    print(f"{bgreen}[3]{reset} 7 Digits Code (150 Threads)")
    print(f"{bgreen}[4]{reset} Pro Code Scanner (Latest)")
    print(f"{bred}[0]{reset} Exit")
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    
    choice = input(f"{yellow}Select Option: {reset}")
    
    try:
        if choice == '1':
            import engcode
            start_tool(engcode, "Eng Mixed")
        elif choice == '2':
            import englow
            start_tool(englow, "Eng Lowercase")
        elif choice == '3':
            import code7
            start_tool(code7, "7 Digits")
        elif choice == '4':
            import procode
            start_tool(procode, "Pro Code")
        elif choice == '0':
            print(f"{yellow}Goodbye!{reset}")
            sys.exit()
        else:
            print(f"{bred}Invalid Choice!{reset}")
            time.sleep(1)
            menu()
    except ImportError as e:
        print(f"{bred}Error: {e.name}.so file not found!{reset}")
        input(f"\n{white}Press Enter to return to menu...{reset}")
        menu()

if __name__ == "__main__":
    menu()
    