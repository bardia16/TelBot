"""Message templates for bot responses."""

START_MESSAGE = """
🤖 *Welcome to the Proxy Channel Collector Bot\!*

I help you collect and validate Telegram proxy channel links\.
Send me links to proxy channels, and I'll validate and store them for the community\.

*Available Commands:*
📝 /start \- Start the bot
❓ /help \- Show supported formats
📋 /list \- Show all collected proxy channels

_Send me some proxy channel links to get started\!_
"""

HELP_MESSAGE = """
*Send me Telegram proxy channel links in any of these formats:*

✅ *Supported formats:*
• `https://t\.me/proxy_channel`
• `https://telegram\.me/proxy_channel`
• `t\.me/proxy_channel`
• `@proxy_channel`

💡 You can send multiple channel links in a single message\!

*Examples:*
`t.me/proxy_example`
`@proxy_channel`
`https://t.me/proxy_links`

_I'll validate each channel and add it to our proxy collection\. 🔍_
"""

INVALID_LINK_FORMAT = """
❌ *Invalid link format*

The link you sent doesn't match any supported format\.
Use /help to see supported formats\.
"""

LINK_VALIDATION_SUCCESS = """
✅ *Success\!*

Successfully validated and stored {0} proxy channel\(s\)\!
Use /list to see all available proxy channels\.
"""

LINK_VALIDATION_PARTIAL = """
⚠️ *Partial Success*

Processed {0} channel\(s\):
✅ Valid: {1}
❌ Invalid: {2}

_Use /list to see all available proxy channels\._
"""

NO_LINKS_FOUND = """
❌ *No Valid Links Found*

I couldn't find any valid Telegram channel links in your message\.
Use /help to see supported formats\.
"""

LIST_LINKS_EMPTY = """
📋 *Available Proxy Channels*

No proxy channels have been collected yet\.
Send me some Telegram proxy channel links to get started\!
"""

LIST_LINKS_HEADER = """
📋 *Available Proxy Channels*

Here are all the available proxy channels:
"""

ERROR_STORAGE = """
⚠️ *Storage Error*

Sorry, I encountered an error while storing the channels\.
Please try again later\.
"""

ERROR_GENERIC = """
⚠️ *Error*

Sorry, something went wrong\. Please try again\.
If the problem persists, contact the bot administrator\.
""" 