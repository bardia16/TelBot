# Telegram Link Collector Bot

A robust Telegram bot that collects, validates, and stores Telegram channel/user links. Built with Python and the python-telegram-bot library.

## Features

- 🔍 **Link Validation**: Validates Telegram links in multiple formats
- 💾 **Persistent Storage**: Stores valid links in JSON format
- 👤 **User Management**: Organizes links by user
- 🔒 **Thread-Safe**: Handles concurrent requests safely
- 🎯 **Error Handling**: Comprehensive error handling and user feedback

## Commands

- `/start` - Initialize the bot and get welcome message
- `/help` - Show supported link formats and usage instructions
- `/list` - Display all your stored links

## Supported Link Formats

The bot accepts Telegram links in the following formats:
```
https://t.me/username
https://telegram.me/username
t.me/username
@username
```

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd telegram_bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add your Telegram bot token:
     ```
     TELEGRAM_BOT_TOKEN=your_bot_token_here
     ```
   - To get a bot token:
     1. Message [@BotFather](https://t.me/BotFather) on Telegram
     2. Use `/newbot` command to create a new bot
     3. Copy the provided token

4. **Run the Bot**
   ```bash
   python main.py
   ```

## Project Structure

```
telegram_bot/
├── bot/
│   ├── __init__.py
│   ├── bot_handler.py      # Core bot functionality
│   └── message_templates.py # Response messages
├── validators/
│   ├── __init__.py
│   └── link_validator.py   # Link validation logic
├── storage/
│   ├── __init__.py
│   └── storage_manager.py  # Data persistence
├── data/
│   └── valid_links.json    # Stored links
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Error Handling

The bot includes comprehensive error handling for various scenarios:

- **Invalid Link Format**: Provides feedback on incorrect link formats
- **Network Issues**: Handles timeouts and connection errors
- **Storage Errors**: Manages file access and data persistence issues
- **API Errors**: Handles Telegram API related issues

## Troubleshooting

Common issues and solutions:

1. **Bot Not Responding**
   - Check if the bot token is correct in `.env`
   - Ensure the bot is running (`python main.py`)
   - Check logs in `bot.log`

2. **Link Validation Fails**
   - Verify the link format (use `/help`)
   - Check if the Telegram entity exists
   - Ensure internet connectivity

3. **Storage Issues**
   - Check write permissions for `data/` directory
   - Verify `valid_links.json` is not corrupted
   - Ensure sufficient disk space

## Logging

The bot logs activities and errors to:
- Console output
- `bot.log` file

Log levels can be configured in `.env`:
```
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code style
- Development setup
- Submission process

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

- Never share your bot token
- Keep the `.env` file secure
- Regularly update dependencies
- Monitor bot activities through logs

## Contact

For issues and feature requests, please use the GitHub issue tracker. 