import os

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ARMS Portal
ARMS_USERNAME = os.environ.get("ARMS_USERNAME", "")
ARMS_PASSWORD = os.environ.get("ARMS_PASSWORD", "")

# Check interval
CHECK_INTERVAL = 900  # 15 minutes