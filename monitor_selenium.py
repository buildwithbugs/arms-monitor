import sys
import signal
from datetime import datetime
from arms_scraper_selenium_fixed import ARMSScraper
from results_db import ResultsDatabase
from telegram_notifier import TelegramNotifier


class ARMSMonitor:
    def __init__(self):
        
        self.scraper  = ARMSScraper()
        self.database = ResultsDatabase()
        self.notifier = TelegramNotifier()
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


        print(f"[{self._ts()}] ── Checking results ──")

        results = self.scraper.scrape_results()

        print("DEBUG → Results fetched:", results)

        if results is None:
            print("[✗] Scraping failed!")
            self.notifier.notify_error("Scraping failed. Check credentials or connection.")

        elif len(results) == 0:
            print("[*] No results published yet.")

        else:
            new = self.database.find_new_results(results)

            print("DEBUG → New results:", new)

            if new:
                print(f"[!] {len(new)} NEW result(s) found!")
                for r in new:
                    self.database.add_result(r)

                    print("DEBUG → Sending Telegram...")

                    self.notifier.send_notification(
                        r['course_code'], r['course_name'],
                        r['grade'], r['status'], r['month_year']
                    )

                    self.database.log_notification(
                        r['course_code'], r['course_name'], r['grade']
                    )
            else:
                print(f"[✓] No new results. ({len(results)} already tracked)")

        self.scraper.close()
        print("[*] Done!")


if __name__ == "__main__":
    monitor = ARMSMonitor()
    monitor.run()