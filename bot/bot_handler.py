"""Core bot handler implementation."""

import logging
from telegram import Update
from telegram.constants import ParseMode
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
    NO_LINKS_FOUND,
    LIST_LINKS_EMPTY,
    LIST_LINKS_HEADER,
    ERROR_STORAGE,
    ERROR_GENERIC
)
from validators.link_validator import LinkValidator
from storage.storage_manager import StorageManager

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
        self.link_validator = LinkValidator()
        self.storage_manager = StorageManager()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register message and command handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(CommandHandler("list", self._list_command))
        
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
        await update.message.reply_text(
            START_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) requested help")
        await update.message.reply_text(
            HELP_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command."""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) requested their links")
        
        # Get user's stored links
        user_data = self.storage_manager.get_user_links(str(user.id))
        
        if not user_data or not user_data.get("links"):
            await update.message.reply_text(
                LIST_LINKS_EMPTY,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        
        # Format links list
        links_text = LIST_LINKS_HEADER
        for i, link in enumerate(user_data["links"], 1):
            # Escape special characters for Markdown
            escaped_link = link.replace(".", "\\.").replace("-", "\\-")
            links_text += f"\n{i}\\. `{escaped_link}`"
        
        await update.message.reply_text(
            links_text,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages with potential links."""
        user = update.effective_user
        message_text = update.message.text
        
        logger.info(f"Received message from user {user.id} ({user.username})")
        
        try:
            # Validate links
            validation_results = self.link_validator.validate_links(message_text)
            
            if not validation_results:
                await update.message.reply_text(
                    NO_LINKS_FOUND,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                return
            
            # Count valid and invalid links
            valid_links = [
                result.normalized_link
                for result in validation_results.values()
                if result.is_valid
            ]
            total_links = len(validation_results)
            valid_count = len(valid_links)
            
            # Store valid links
            if valid_links:
                stored = self.storage_manager.store_links(
                    str(user.id),
                    user.username or "",
                    valid_links
                )
                if not stored:
                    logger.error(f"Failed to store links for user {user.id}")
                    await update.message.reply_text(
                        ERROR_STORAGE,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                    return
            
            # Prepare response message
            if valid_count == 0:
                await update.message.reply_text(
                    NO_LINKS_FOUND,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            elif valid_count == total_links:
                await update.message.reply_text(
                    LINK_VALIDATION_SUCCESS.format(valid_count),
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            else:
                await update.message.reply_text(
                    LINK_VALIDATION_PARTIAL.format(
                        total_links,
                        valid_count,
                        total_links - valid_count
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(
                ERROR_GENERIC,
                parse_mode=ParseMode.MARKDOWN_V2
            )
    
    async def _error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Error occurred: {context.error}")
        if update and hasattr(update, 'effective_message'):
            await update.effective_message.reply_text(
                ERROR_GENERIC,
                parse_mode=ParseMode.MARKDOWN_V2
            )
    
    def run(self):
        """Run the bot."""
        logger.info("Starting bot...")
        self.application.run_polling() 