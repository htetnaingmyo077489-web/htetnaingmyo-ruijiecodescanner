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
    print(f"{white}           STARLINK ALL-IN-ONE SCANNER          {reset}")
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    print(f"{bgreen}[1]{reset} ENG&NUMBER6")
    print(f"{bgreen}[2]{reset} ENG LOWERCASE6")
    print(f"{bgreen}[3]{reset} NUMBER CODE7")
    print(f"{bgreen}[4]{reset} NUMBER CODE6")
    print(f"{bred}[0]{reset} EXIT")
    print(f"{bcyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{reset}")
    
    choice = input(f"{yellow} SELECT OPTION: {reset}")
    
    try:
        if choice == '1':
            import engcode
            start_tool(engcode, "ENG&NUMBER6")
        elif choice == '2':
            import englow
            start_tool(englow, "ENG LOWERCASE6")
        elif choice == '3':
            import code7
            start_tool(code7, "NUMBER CODE7")
        elif choice == '4':
            import procode
            start_tool(procode, "NUMBER CODE6")
        elif choice == '0':
            print(f"{yellow}GOODBYE!{reset}")
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
    