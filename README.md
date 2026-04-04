\# 🎓 ARMS Portal Monitor

**Automated result monitoring system for Saveetha ARMS Portal that sends instant Telegram notifications when new results are published.**

> ⭐ **Star this repo if it helps you stay updated with your results!



\## 📱 Features

- **🔄 Automatic Monitoring** - Checks ARMS portal every 15 minutes
- **⚡ Instant Notifications** - Real-time Telegram alerts for new results
- **🛡️ Smart Deduplication** - Never sends duplicate notifications
- **☁️ 24/7 Operation** - Runs continuously on GitHub Actions (no laptop needed)
- **🎯 Zero Maintenance** - Set it once and forget it
- **📊 Result Tracking** - Maintains history of all your results
- **🔒 Secure & Private** - All credentials stored in GitHub Secrets



\## 🎯 How It Works

1. **Login Automation** - Selenium automatically logs into ARMS portal
2. **Result Scraping** - Extracts latest results from dashboard
3. **Change Detection** - Compares with database to find new results
4. **Instant Alerts** - Sends Telegram notification for new results
5. **Database Update** - Stores results to prevent duplicate notifications



\## 🛠️ Tech Stack

- **Python 3.11** - Core language
- **Selenium** - Web automation for portal scraping
- **SQLite** - Local database for result tracking
- **Telegram Bot API** - Instant notifications
- **GitHub Actions** - 24/7 cloud deployment
- **Chrome Headless** - Browser automation



\## 📂 Project Structure

```
Arms_Monitor/
├── monitor_selenium.py           # Main entry point
├── arms_scraper_selenium_fixed.py  # Portal scraper
├── telegram_notifier.py         # Telegram notifications
├── results_db.py               # Database handler
├── config.py                   # Configuration management
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── .github/workflows/monitor.yml  # GitHub Actions workflow
└── README.md                  # This file
```



\## 🚀 Quick Start

### For Saveetha Students
1. **Fork this repository**
2. **Set up GitHub Secrets** in your fork:
   - `TELEGRAM_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
   - `TELEGRAM_CHAT_ID` - Get from [@userinfobot](https://t.me/userinfobot)
   - `ARMS_USERNAME` - Your student ID (e.g., `192511060`)
   - `ARMS_PASSWORD` - Your ARMS portal password
3. **Enable GitHub Actions** in your repository settings
4. **That's it!** The bot will monitor your results every 15 minutes

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your credentials
4. Run: `python monitor_selenium.py`



\## ⚙️ Configuration

### Environment Variables
Create a `.env` file locally (or use GitHub Secrets for production):

```bash
# ARMS Portal Credentials
ARMS_USERNAME=your_student_id
ARMS_PASSWORD=your_arms_password

# Telegram Bot Settings
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Setting up Telegram Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token
4. Message your bot to start a chat
5. Get your chat ID from [@userinfobot](https://t.me/userinfobot)

## 🚨 Important Notes

- **Security**: Never commit your `.env` file or share credentials
- **Frequency**: GitHub Actions runs every 15 minutes (can't be more frequent)
- **Database**: `results.db` is committed to track results across runs
- **Compatibility**: Works specifically for Saveetha ARMS Portal

## 🤝 Contributing

Feel free to:
- 🐛 Report issues
- 💡 Suggest features
- 🔧 Submit pull requests
- ⭐ Star the repository

## 📄 License

This project is open source. Feel free to fork and modify for your educational institution.

## 👨‍💻 Developer

**Manoj M**
Saveetha School of Engineering, SIMATS

---

> 💡 **Tip**: If you're from a different institution, you can adapt the scraper for your portal!
# Updated 04/04/2026 10:06:06
# Updated 04/04/2026 10:22:51
