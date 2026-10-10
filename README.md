# Telegram Media & Story Downloader Bot

A powerful Python tool built with **Telethon** (Telegram MTProto client) that connects to your Telegram account and downloads videos, photos, captions, and upload dates from links, stories, and channel histories.

---

## Features

- 🔐 **Account Sign-in (MTProto)**: Uses your personal Telegram account credentials (`api_id`, `api_hash`, phone/session) via Telethon to access public and private content (stories, channels).
- 🔗 **Post Link Downloader**: Send any post link (`https://t.me/channel/123` or `https://t.me/c/1234567890/123`) to download videos, photos, captions, and original upload date.
- 📸 **Story Downloader from Link**: Send any story link (`https://t.me/username/s/12`) to download video/photo stories.
- 👤 **User Stories by Username / ID**:
  - `/user_stories @username 24h` — Download only stories posted in the **last 24 hours**.
  - `/user_stories @username all` — Download **all active public stories**.
- 📢 **Channel Batch Downloader**:
  - `/channel @channel_name` or `/channel -1001234567890` — Iterates through the channel and downloads all media posts with captions and timestamps.
- 📝 **Metadata Preservation**: Saves a clean JSON sidecar alongside each downloaded media file containing the caption, upload timestamp (ISO 8601), message/story ID, and view counts.

---

## Quick Setup

### 1. Requirements

Install required dependencies (if not already installed):
```bash
pip install telethon python-dotenv pytest
```

### 2. Configure Credentials

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your API credentials from [my.telegram.org](https://my.telegram.org):
```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef0123456789abcdef0123456789
TELEGRAM_PHONE=+1234567890
# Optional: If you also want to respond via a Bot token
TELEGRAM_BOT_TOKEN=
TELEGRAM_SESSION_NAME=user_account_session
DOWNLOAD_DIR=downloads
```

### 3. Authenticate Session

Authenticate your account interactively once:
```bash
python src/telebot_downloader/main.py --auth
```
This requests a Telegram verification code, saves `user_account_session.session`, and logs you in.

---

## How to Use

### Mode A: Run Interactive Bot Service

Start the bot service:
```bash
python src/telebot_downloader/main.py --run
```
Now send links or commands to your bot/account:
- Post link: `https://t.me/telegram/1234`
- Story link: `https://t.me/durov/s/12`
- User stories (last 24h): `/user_stories durov 24h`
- User stories (all): `/user_stories durov all`
- Channel posts: `/channel @tech_channel`

### Mode B: Direct CLI Download

You can also download directly from the command line without keeping the bot service running:
```bash
# Download a post
python src/telebot_downloader/main.py --download "https://t.me/telegram/1234"

# Download a story
python src/telebot_downloader/main.py --download "https://t.me/durov/s/12"

# Download user stories from the last 24 hours
python src/telebot_downloader/main.py --download "/user_stories durov 24h"

# Download all channel media posts
python src/telebot_downloader/main.py --download "/channel @telegram"
```

---

## Running Automated Tests

Run the full pytest suite:
```bash
pytest
```
All 16 unit tests test parser URL handling, 24-hour story filtering, metadata extraction, and command routing.
