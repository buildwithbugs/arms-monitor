# ─────────────────────────────────────────
#  ARMS PORTAL CREDENTIALS
# ─────────────────────────────────────────
ARMS_URL = "https://arms.sse.saveetha.com/"
ARMS_USERID  = "192511060"
ARMS_PASSWORD = "mano"

# ─────────────────────────────────────────
#  TELEGRAM BOT SETTINGS (from environment)
# ─────────────────────────────────────────
import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ─────────────────────────────────────────
#  MONITOR SETTINGS
# ─────────────────────────────────────────
CHECK_INTERVAL = 5 * 60   # Check every 5 minutes
DATABASE_NAME  = "results.db"