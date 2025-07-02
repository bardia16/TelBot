"""Main entry point for the Telegram Link Collector Bot."""

import os
from dotenv import load_dotenv
from bot.bot_handler import BotHandler

def main():
    """Initialize and run the bot."""
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    # Initialize and run bot
    bot = BotHandler(token)
    bot.run()

if __name__ == '__main__':
    main()
