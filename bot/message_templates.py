"""Message templates for bot responses."""

START_MESSAGE = """
Welcome to the Telegram Link Collector Bot! 🤖

I can help you collect and validate Telegram channel/user links.
Just send me any Telegram links and I'll validate and store them.

Use /help to see supported link formats.
"""

HELP_MESSAGE = """
Send me Telegram links in any of these formats:

✅ Supported formats:
• https://t.me/username
• https://telegram.me/username
• t.me/username
• @username

You can send multiple links in a single message!

Examples:
t.me/example
@example
https://t.me/example

I'll validate each link and store the valid ones. 🔍
"""

INVALID_LINK_FORMAT = "❌ Invalid link format. Use /help to see supported formats."

LINK_VALIDATION_SUCCESS = "✅ Successfully validated and stored {} links!"

LINK_VALIDATION_PARTIAL = "⚠️ Processed {} links:\n✅ Valid: {}\n❌ Invalid: {}"

NO_LINKS_FOUND = "❌ No valid Telegram links found in your message. Use /help to see supported formats." 