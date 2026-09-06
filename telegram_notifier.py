import requests
from datetime import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api = f"https://api.telegram.org/bot{self.token}" if self.token else None
        self.enabled = bool(self.token and self.chat_id)

        if not self.token:
            print("[WARNING] TELEGRAM_TOKEN environment variable is not set - Telegram notifications disabled")
        if not self.chat_id:
            print("[WARNING] TELEGRAM_CHAT_ID environment variable is not set - Telegram notifications disabled")

        if self.enabled:
            self.chat_id = str(self.chat_id)
            print(f"[DEBUG] Telegram notifier initialized for chat_id={self.chat_id}")
        else:
            print("[INFO] Telegram notifications are disabled (missing environment variables)")

    def _send(self, text):
        if not self.enabled:
            print(f"[SKIP] Telegram disabled - would send: {text[:50]}...")
            return True

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
            }
            r = requests.post(f"{self.api}/sendMessage", json=payload, timeout=10)

            if r.status_code == 200:
                response_data = r.json()
                if response_data.get("ok"):
                    print("[✓] Telegram message sent successfully")
                    return True
                print(f"[✗] Telegram API returned error: {response_data.get('description', 'Unknown error')}")
                return False

            print(f"[✗] Telegram API request failed with status {r.status_code}")
            return False

        except requests.exceptions.Timeout:
            print("[✗] Telegram request timed out (10s)")
            return False
        except requests.exceptions.ConnectionError:
            print("[✗] Telegram connection error - check internet/network")
            return False
        except Exception as e:
            print(f"[✗] Telegram error: {e}")
            return False

    def test_connection(self):
        if not self.enabled:
            print("[SKIP] Telegram disabled - skipping connection test")
            return False

        try:
            r = requests.get(f"{self.api}/getMe", timeout=10)
            if r.status_code == 200:
                response_data = r.json()
                if response_data.get("ok"):
                    name = response_data["result"]["first_name"]
                    print(f"[✓] Telegram connected — Bot: {name}")
                    return True
                print(f"[✗] Telegram API returned error: {response_data.get('description', 'Unknown error')}")
                return False
            print(f"[✗] Telegram getMe failed with status {r.status_code}")
            return False
        except requests.exceptions.Timeout:
            print("[✗] Telegram test timed out (10s)")
            return False
        except requests.exceptions.ConnectionError:
            print("[✗] Telegram connection error - check internet/network")
            return False
        except Exception as e:
            print(f"[✗] Telegram test failed: {e}")
            return False

    def notify_start(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_message = (
            "🚀 <b>VStudy Monitor Started</b>\n"
            f"🕐 {now}\n\n"
            "I'll notify you when a new course result is published. 📡"
        )
        return self._send(start_message)

    def send_notification(self, course_code, course_name, grade="", status="", month_year="", course_type="", course_gpa=""):
        message = (
            "NEW RESULT PUBLISHED\n\n"
            f"Course: {course_name}\n"
            f"Code: {course_code}\n"
            f"Type: {course_type or 'N/A'}\n"
            f"Status: {status or 'N/A'}\n"
            f"Grade: {grade or 'N/A'}\n"
            f"Course GPA: {course_gpa or 'N/A'}"
        )

        print(f"[INFO] Attempting to send notification for course: {course_code}")
        sent = self._send(message)
        if sent:
            print(f"[✓] Notification sent successfully for {course_code}")
        else:
            print(f"[✗] Failed to send notification for {course_code}")
        return sent

    def notify_error(self, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"⚠️ <b>VStudy Monitor Error</b>\n🕐 {now}\n\n❌ {msg}"
        print(f"[INFO] Sending error notification: {msg}")
        sent = self._send(error_message)
        if sent:
            print("[✓] Error notification sent successfully")
        else:
            print("[✗] Failed to send error notification")
        return sent