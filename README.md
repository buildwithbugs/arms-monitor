# VStudy Course Monitor

This project monitors the Saveetha VStudy portal, collects the course table, detects new course results by course code, stores the history in SQLite, and sends Telegram notifications for new results.

## Features

- Persistent Chrome profile for manual Google sign-in once
- VStudy profile page and View Details flow
- Student Progress filtering for All 17 courses
- Course extraction and deduplication by course code
- SQLite result and notification history
- Telegram notifications for newly detected courses

## Required environment variables

Create a `.env` file with:

```bash
VSTUDY_URL=https://vstudy.saveetha.com/
VSTUDY_PROFILE_DIR=./vstudy_chrome_profile
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
DATABASE_NAME=./results.db
```

## Project structure

```text
.
├── config.py
├── monitor.py
├── monitor_selenium.py
├── vstudy_scraper.py
├── results_db.py
├── telegram_notifier.py
├── requirements.txt
├── .env.example
├── README.md
├── results.db
├── vstudy_chrome_profile/
└── test_vstudy_login.py
```

## How it works

1. Open the VStudy portal using the configured persistent Chrome profile.
2. Navigate to the student profile page.
3. Click View Details.
4. Select the All 17 filter in Student Progress.
5. Parse the course table and collect unique course codes.
6. Store the results in SQLite and notify only when a new course code is seen.

## Run locally

```bash
pip install -r requirements.txt
python monitor.py
```

## Deploy on Railway

Railway can run the monitor without human clicks after an authenticated Chrome profile has been prepared. Google login, CAPTCHA, and account verification cannot be completed automatically by this project.

1. Build and deploy this repository using the included `Dockerfile`.
2. Add a Railway volume mounted at `/data`.
3. Set these variables in Railway:

```text
HEADLESS=true
UNATTENDED=true
RUN_FOREVER=true
VSTUDY_PROFILE_DIR=/data/vstudy_chrome_profile
DATABASE_NAME=/data/results.db
CHECK_INTERVAL=300
SAVE_DEBUG_ARTIFACTS=false
VSTUDY_URL=https://vstudy.saveetha.com/
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Before unattended deployment, copy an already authenticated Chrome profile into the persistent volume at `/data/vstudy_chrome_profile`. If the Google session expires, the profile must be re-authenticated and the volume updated. Without that profile, the service fails clearly instead of waiting for a human prompt.

When re-authentication is needed, the monitor prints `[AUTH REQUIRED]` in Railway logs and sends one Telegram warning. It keeps retrying at `CHECK_INTERVAL` and sends no duplicate warning until authentication works again. This lets you know exactly why no new results are being collected.

The warning state is stored in the SQLite `monitor_state` table, so a Railway restart does not cause repeated alerts. A successful scrape resets the state and allows a new warning if authentication expires later. Set `SAVE_DEBUG_ARTIFACTS=true` only when troubleshooting; it is disabled by default for live deployments.

There is no reliable browser-only way to guarantee zero human interaction forever with Google login. A truly zero-interaction design would require VStudy to provide an official API or a long-lived service credential. Do not deploy Google passwords or CAPTCHA workarounds in Railway.

For a one-time local check, use `python test_vstudy_login.py`. A successful check prints `Found ... course(s)` and exits with code 0; an authentication or scraping failure exits with code 1.

## Notes

- The project intentionally keeps the persistent browser profile for authenticated VStudy access.
- Telegram notifications remain optional and are enabled only when the token and chat ID are configured.
- The SQLite database preserves the notification history and deduplicates by course code.
