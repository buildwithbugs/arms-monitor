import time
import sys
import signal
from datetime import datetime
from arms_scraper_selenium_fixed import ARMSScraper
from results_db import ResultsDatabase
from telegram_notifier import TelegramNotifier
from config import CHECK_INTERVAL


class ARMSMonitor:
    def __init__(self):
        self.scraper  = ARMSScraper()
        self.database = ResultsDatabase()
        self.notifier = TelegramNotifier()
        self.running  = True
        self.count    = 0
        signal.signal(signal.SIGINT, self._on_exit)

    def _on_exit(self, sig, frame):
        print("\n[!] Stopping monitor...")
        self.scraper.close()
        sys.exit(0)

    def _ts(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run(self):
        print("=" * 55)
        print("   ARMS RESULT MONITOR — TELEGRAM NOTIFICATIONS")
        print("=" * 55)

        if not self.notifier.test_connection():
            print("[!] Telegram not connected — check your token/chat ID")

        self.notifier.notify_start()
        print(f"[*] Checking every {CHECK_INTERVAL // 60} minutes. Press Ctrl+C to stop.\n")

        while self.running:
            self.count += 1
            print(f"\n[{self._ts()}] ── Check #{self.count} ──")

            results = self.scraper.scrape_results()

            if results is None:
                print("[✗] Scraping failed, will retry...")
                self.notifier.notify_error("Scraping failed. Check credentials or connection.")
            elif len(results) == 0:
                print("[*] No results published yet.")
            else:
                new = self.database.find_new_results(results)
                if new:
                    print(f"[!] {len(new)} NEW result(s) found!")
                    for r in new:
                        self.database.add_result(r)
                        self.notifier.send_notification(
                            r['course_code'], r['course_name'],
                            r['grade'], r['status'], r['month_year']
                        )
                        self.database.log_notification(r['course_code'], r['course_name'], r['grade'])
                else:
                    print(f"[✓] No new results. ({len(results)} already tracked)")

            print(f"[*] Next check in {CHECK_INTERVAL // 60} min...")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    ARMSMonitor().run()