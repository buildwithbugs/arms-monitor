import requests
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:
    def __init__(self):
        self.token   = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api     = f"https://api.telegram.org/bot{self.token}"

    def _send(self, text):
        try:
            r = requests.post(
                f"{self.api}/sendMessage",
                json={"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"},
                timeout=10
            )
            return r.status_code == 200
        except Exception as e:
            print(f"[✗] Telegram error: {e}")
            return False

    def test_connection(self):
        try:
            r = requests.get(f"{self.api}/getMe", timeout=10)
            if r.status_code == 200:
                name = r.json()["result"]["first_name"]
                print(f"[✓] Telegram connected — Bot: {name}")
                return True
            print(f"[✗] Telegram token invalid")
            return False
        except Exception as e:
            print(f"[✗] Telegram test failed: {e}")
            return False

    def notify_start(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._send(
            f"🚀 <b>ARMS Monitor Started</b>\n"
            f"🕐 {now}\n\n"
            f"I'll ping you the moment your results are published! 📡"
        )
        print("[✓] Startup notification sent")

    def send_notification(self, course_code, course_name, grade, status, month_year):
        sent = self._send(
            f"🎓 <b>NEW RESULT PUBLISHED!</b>\n\n"
            f"📘 <b>Course:</b> {course_name}\n"
            f"🔖 <b>Code:</b> {course_code}\n"
            f"🏆 <b>Grade:</b> {grade}\n"
            f"✅ <b>Status:</b> {status}\n"
            f"📅 <b>Month/Year:</b> {month_year}\n\n"
            f"Check your ARMS portal now! 🎉"
        )
        if sent:
            print(f"[✓] Notification sent for {course_code}")

    def notify_error(self, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._send(f"⚠️ <b>ARMS Monitor Error</b>\n🕐 {now}\n\n❌ {msg}")