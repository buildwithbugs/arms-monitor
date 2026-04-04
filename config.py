# ─────────────────────────────────────────
#  ARMS PORTAL CREDENTIALS (from environment)
# ─────────────────────────────────────────
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

ARMS_URL = "https://arms.sse.saveetha.com/"
ARMS_USERID  = os.getenv("ARMS_USERNAME", "")
ARMS_PASSWORD = os.getenv("ARMS_PASSWORD", "")

# ─────────────────────────────────────────
#  TELEGRAM BOT SETTINGS (from environment)
# ─────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ─────────────────────────────────────────
#  MONITOR SETTINGS
# ─────────────────────────────────────────
CHECK_INTERVAL = 5 * 60   # Check every 5 minutes
DATABASE_NAME  = "results.db"