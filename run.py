import engcode
import threading
import time

if __name__ == "__main__":
    if engcode.check_approval():
        try:
            threading.Thread(target=engcode.background_key_verification, daemon=True).start()
            threading.Thread(target=engcode.session_refiller, daemon=True).start()
            threading.Thread(target=engcode.live_dashboard, daemon=True).start()
            for _ in range(engcode.NUM_THREADS):
                threading.Thread(target=engcode.worker_thread, daemon=True).start()
            while True: time.sleep(1)
        except KeyboardInterrupt:
            engcode.stop_event.set()
            print("\nStopping...")
            