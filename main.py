import procode

if __name__ == "__main__":
    if procode.check_approval():
        try:
            import threading
            import time
            
            threading.Thread(target=procode.background_key_verification, daemon=True).start()
            threading.Thread(target=procode.session_refiller, daemon=True).start()
            threading.Thread(target=procode.live_dashboard, daemon=True).start()
            
            for _ in range(procode.NUM_THREADS):
                threading.Thread(target=procode.worker_thread, daemon=True).start()
            
            while True: time.sleep(1)
        except KeyboardInterrupt:
            procode.stop_event.set()
            print("\nStopping...")

