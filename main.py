"""Main entry point for the Telegram Link Collector Bot."""

import os
import sys
import signal
import logging
from dotenv import load_dotenv
from bot.bot_handler import BotHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal. Cleaning up...")
    sys.exit(0)

def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def check_environment():
    """Check and validate environment variables."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        logger.error("Please create a .env file with your bot token")
        sys.exit(1)
    return token

def main():
    """Initialize and run the bot."""
    try:
        # Setup signal handlers
        setup_signal_handlers()
        
        # Load environment variables
        logger.info("Loading environment variables...")
        load_dotenv()
        
        # Check environment
        token = check_environment()
        
        # Initialize bot
        logger.info("Initializing bot...")
        bot = BotHandler(token)
        
        # Run bot
        logger.info("Starting bot...")
        bot.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
