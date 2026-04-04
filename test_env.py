#!/usr/bin/env python3
import os

print("=== Environment Variable Test ===")
print(f"ARMS_USERNAME: {'SET' if os.getenv('ARMS_USERNAME') else 'NOT SET'}")
print(f"ARMS_PASSWORD: {'SET' if os.getenv('ARMS_PASSWORD') else 'NOT SET'}")
print(f"TELEGRAM_TOKEN: {'SET' if os.getenv('TELEGRAM_TOKEN') else 'NOT SET'}")
print(f"TELEGRAM_CHAT_ID: {'SET' if os.getenv('TELEGRAM_CHAT_ID') else 'NOT SET'}")

# Test config loading
try:
    from config import ARMS_USERID, ARMS_PASSWORD, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    print("\n=== Config Loading Test ===")
    print(f"ARMS_USERID length: {len(ARMS_USERID) if ARMS_USERID else 0}")
    print(f"ARMS_PASSWORD length: {len(ARMS_PASSWORD) if ARMS_PASSWORD else 0}")
    print(f"TELEGRAM_TOKEN length: {len(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else 0}")
    print(f"TELEGRAM_CHAT_ID length: {len(TELEGRAM_CHAT_ID) if TELEGRAM_CHAT_ID else 0}")
except Exception as e:
    print(f"Config loading error: {e}")
