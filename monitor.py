import time

from config import CHECK_INTERVAL, RUN_FOREVER
from monitor_selenium import VStudyMonitor


if __name__ == "__main__":
    monitor = VStudyMonitor()
    while True:
        try:
            monitor.run()
        except Exception as exc:
            print(f"[✗] Monitor cycle failed: {exc}")
            if not RUN_FOREVER:
                raise
        if not RUN_FOREVER:
            break
        print(f"[*] Next check in {CHECK_INTERVAL} seconds")
        time.sleep(CHECK_INTERVAL)
