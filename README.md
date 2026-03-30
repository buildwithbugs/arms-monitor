\# 🎓 ARMS Portal Monitor



Automated result monitoring system for Saveetha ARMS Portal that sends instant Telegram notifications when new results are published.



\## 📱 Features



\- Monitors ARMS portal every 15 minutes automatically

\- Sends instant Telegram notification when new results are published

\- Runs 24/7 on GitHub Actions — no laptop required

\- Tracks already-notified results to avoid duplicates

\- Headless Chrome browser automation using Selenium



\## 🛠️ Tech Stack



\- Python 3.11

\- Selenium (web scraping)

\- SQLite (result tracking)

\- Telegram Bot API (notifications)

\- GitHub Actions (24/7 scheduling)



\## 📂 Project Structure



Arms\_Monitor/

├── monitor\_selenium.py        # Main entry point

├── arms\_scraper\_selenium\_fixed.py  # Portal scraper

├── telegram\_notifier.py       # Telegram notifications

├── results\_db.py              # Database handler

├── config.py                  # Configuration

├── requirements.txt           # Dependencies

└── .github/

&#x20;   └── workflows/

&#x20;       └── monitor.yml        # GitHub Actions workflow

```



\## ⚙️ Setup



1\. Clone the repository

2\. Add GitHub Secrets:

&#x20;  - `TELEGRAM\_TOKEN`

&#x20;  - `TELEGRAM\_CHAT\_ID`

&#x20;  - `ARMS\_USERNAME`

&#x20;  - `ARMS\_PASSWORD`

3\. Enable GitHub Actions

4\. Workflow runs automatically every 15 minutes!



\## 👨‍💻 Developer



\*\*Manoj M\*\*

Saveetha School of Engineering, SIMATS

