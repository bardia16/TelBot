"""Message templates for bot responses."""

START_MESSAGE = """
🤖 *Welcome to the Telegram Link Collector Bot\!*

I can help you collect and validate Telegram channel/user links\.
Just send me any Telegram links and I'll validate and store them\.

*Available Commands:*
📝 /start \- Start the bot
❓ /help \- Show supported formats
📋 /list \- Show your stored links

_Send me some links to get started\!_
"""

HELP_MESSAGE = """
*Send me Telegram links in any of these formats:*

✅ *Supported formats:*
• `https://t\.me/username`
• `https://telegram\.me/username`
• `t\.me/username`
• `@username`

💡 You can send multiple links in a single message\!

*Examples:*
`t.me/example`
`@example`
`https://t.me/example`

_I'll validate each link and store the valid ones\. 🔍_
"""

INVALID_LINK_FORMAT = """
❌ *Invalid link format*

The link you sent doesn't match any supported format\.
Use /help to see supported formats\.
"""

LINK_VALIDATION_SUCCESS = """
✅ *Success\!*

Successfully validated and stored {0} link\(s\)\!
Use /list to see all your stored links\.
"""

LINK_VALIDATION_PARTIAL = """
⚠️ *Partial Success*

Processed {0} link\(s\):
✅ Valid: {1}
❌ Invalid: {2}

_Use /list to see all your stored links\._
"""

NO_LINKS_FOUND = """
❌ *No Valid Links Found*

I couldn't find any valid Telegram links in your message\.
Use /help to see supported formats\.
"""

LIST_LINKS_EMPTY = """
📋 *Your Stored Links*

You don't have any stored links yet\.
Send me some Telegram links to get started\!
"""

LIST_LINKS_HEADER = """
📋 *Your Stored Links*

Here are all your stored links:
"""

ERROR_STORAGE = """
⚠️ *Storage Error*

Sorry, I encountered an error while storing your links\.
Please try again later\.
"""

ERROR_GENERIC = """
⚠️ *Error*

Sorry, something went wrong\. Please try again\.
If the problem persists, contact the bot administrator\.
""" 