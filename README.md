# Telegram Link Collector Bot

A Telegram bot that collects, validates, and stores Telegram channel/user links.

## Features

- Collects Telegram channel and user links
- Validates link format and existence
- Stores valid links per user
- Supports multiple links per message
- User-friendly command interface

## Commands

- `/start` - Start the bot and get welcome message
- `/help` - Show usage instructions and link format

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```
4. Run the bot:
```bash
python main.py
```

## Project Structure

```
telegram_bot/
├── bot/
│   ├── __init__.py
│   ├── bot_handler.py
│   └── message_templates.py
├── validators/
│   ├── __init__.py
│   └── link_validator.py
├── storage/
│   ├── __init__.py
│   └── storage_manager.py
├── data/
│   └── valid_links.json
├── main.py
├── requirements.txt
└── README.md
```

## Link Format

The bot accepts Telegram links in the following formats:
- `https://t.me/username`
- `https://telegram.me/username`
- `t.me/username`
- `@username`

Multiple links can be sent in a single message.

## Storage

Valid links are stored in `data/valid_links.json` with the following structure:
```json
{
  "user_id": {
    "username": "user_telegram_username",
    "links": [
      "https://t.me/example1",
      "https://t.me/example2"
    ]
  }
}
``` 