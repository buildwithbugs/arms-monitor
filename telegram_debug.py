#!/usr/bin/env python3
"""
Telegram Debug Script
Run this to test your Telegram bot setup locally.
"""

import os
import requests

def test_telegram_connection():
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        print("❌ TELEGRAM_TOKEN environment variable not set")
        return False

    if not chat_id:
        print("❌ TELEGRAM_CHAT_ID environment variable not set")
        return False

    print(f"🔑 Token: {token[:10]}...")
    print(f"💬 Chat ID: {chat_id}")

    # Test bot connection
    api_url = f"https://api.telegram.org/bot{token}"
    print("\n📡 Testing bot connection...")

    try:
        r = requests.get(f"{api_url}/getMe", timeout=10)
        print(f"📊 getMe Status: {r.status_code}")
        print(f"📄 Response: {r.text}")

        if r.status_code == 200:
            data = r.json()
            if data.get("ok"):
                bot_name = data["result"]["first_name"]
                print(f"✅ Bot connected: {bot_name}")
            else:
                print(f"❌ Bot error: {data.get('description')}")
                return False
        else:
            print(f"❌ HTTP error: {r.status_code}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

    # Test sending message
    print("\n📨 Testing message send...")
    payload = {
        "chat_id": str(chat_id),
        "text": "🧪 Test message from ARMS Monitor debug script",
        "parse_mode": "HTML"
    }

    try:
        r = requests.post(f"{api_url}/sendMessage", json=payload, timeout=10)
        print(f"📊 sendMessage Status: {r.status_code}")
        print(f"📄 Response: {r.text}")

        if r.status_code == 200:
            data = r.json()
            if data.get("ok"):
                print("✅ Test message sent successfully!")
                return True
            else:
                print(f"❌ Send error: {data.get('description')}")
                return False
        else:
            print(f"❌ HTTP error: {r.status_code}")
            return False

    except Exception as e:
        print(f"❌ Send error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 ARMS Monitor - Telegram Debug Tool")
    print("=" * 50)

    success = test_telegram_connection()

    if success:
        print("\n🎉 All tests passed! Your Telegram setup is working.")
    else:
        print("\n❌ Tests failed. Check your configuration:")
        print("   1. TELEGRAM_TOKEN from BotFather")
        print("   2. TELEGRAM_CHAT_ID (get from @userinfobot or your bot)")
        print("   3. Bot added to your Telegram channel/group")
        print("   4. Internet connection")
        