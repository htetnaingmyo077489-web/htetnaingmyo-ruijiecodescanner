import englow

if __name__ == "__main__":
    if englow.check_approval():
        try:
            import threading
            import time
            
            threading.Thread(target=englow.background_key_verification, daemon=True).start()
            threading.Thread(target=englow.session_refiller, daemon=True).start()
            threading.Thread(target=englow.live_dashboard, daemon=True).start()
            
            for _ in range(englow.NUM_THREADS):
                threading.Thread(target=englow.worker_thread, daemon=True).start()
            
            while True: time.sleep(1)
        except KeyboardInterrupt:
            englow.stop_event.set()
            print("\nStopping...")