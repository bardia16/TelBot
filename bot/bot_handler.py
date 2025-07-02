"""Core bot handler implementation."""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from .message_templates import (
    START_MESSAGE,
    HELP_MESSAGE,
    INVALID_LINK_FORMAT,
    LINK_VALIDATION_SUCCESS,
    LINK_VALIDATION_PARTIAL,
    NO_LINKS_FOUND
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotHandler:
    """Handles all bot operations and message routing."""
    
    def __init__(self, token: str):
        """Initialize bot with token."""
        self.application = Application.builder().token(token).build()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register message and command handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        
        # Message handler for links
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )
        
        # Error handler
        self.application.add_error_handler(self._error_handler)
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) started the bot")
        await update.message.reply_text(START_MESSAGE)
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) requested help")
        await update.message.reply_text(HELP_MESSAGE)
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages with potential links."""
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Received message from user {user.id} ({user.username})")
        # This is a placeholder - actual link processing will be implemented later
        await update.message.reply_text(
            "Message received! Link processing will be implemented in the next steps."
        )
    
    async def _error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Error occurred: {context.error}")
        
    def run(self):
        """Run the bot."""
        logger.info("Starting bot...")
        self.application.run_polling() 