import os

# ARMS
ARMS_URL = "https://arms.sse.saveetha.com/"
ARMS_USERNAME = os.getenv("ARMS_USERNAME")
ARMS_PASSWORD = os.getenv("ARMS_PASSWORD")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Monitor
CHECK_INTERVAL = 5 * 60
DATABASE_NAME = "results.db"