import telegram
import config
import asyncio # Ensure asyncio is imported

async def send_telegram_message(message_text):
    bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=message_text,
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
        )
        print("Message sent successfully with MarkdownV2!")
        return True
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram message with MarkdownV2: {e}")
        if "escape" in str(e).lower() or "can't parse entities" in str(e).lower():
            print("MarkdownV2 parsing error. Consider escaping special characters.")
            print("Attempting to send as plain text...")
            try:
                await bot.send_message(
                    chat_id=config.TELEGRAM_CHAT_ID,
                    text=message_text # Send as plain text
                )
                print("Message sent successfully as plain text after MarkdownV2 error.")
                return True
            except Exception as plain_e:
                print(f"Error sending Telegram message as plain text: {plain_e}")
                return False
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == '__main__':
    # For testing the function directly
    # Ensure your config.py is set up with valid TOKEN and CHAT_ID
    
    # Import format_message for a more realistic test, but be cautious about escaping
    # from message_formatter import format_message # Assuming this is in the same directory or PYTHONPATH

    # Test message with MarkdownV2 characters.
    # Characters like '.', '-', '!', '(', ')', etc., must be escaped with a preceding '\'.
    # Example: "Hello\. This is a test message\!"
    # Our formatter currently produces '*' for bold and uses '\n' for newlines.
    
    # A simple, manually escaped MarkdownV2 message for initial testing:
    escaped_title = "Tesla *Delivers* Record Cars \- Stock Jumps\!" 
    # Note: AlphaVantage and NewsAPI might return strings with special characters.
    # These would need to be escaped before being inserted into f-strings for MarkdownV2.
    
    test_msg_markdown_safe = f"Tesla Stock: $180\\.50\\n\\n--- News ---\\n1\\. *{escaped_title}*\\n   http://example\\.com/news"
    
    # A message that is likely to fail MarkdownV2 parsing if not careful:
    # This message contains unescaped characters like '.', '!', and uses '*' for bold.
    # The message_formatter.py currently creates messages like this.
    test_msg_likely_to_fail_markdown = "Tesla Stock: $175.50\n\n--- News ---\n1. *Tesla Q1 Earnings Call Highlights!*\n   http://example.com/q1-highlights"

    async def main_test():
        print(f"Attempting to send test message to chat ID: {config.TELEGRAM_CHAT_ID}")
        
        print("\n--- Test 1: Sending pre-escaped MarkdownV2 message ---")
        success_safe = await send_telegram_message(test_msg_markdown_safe)
        if success_safe:
            print("Pre-escaped MarkdownV2 test message sent/handled.")
        else:
            print("Pre-escaped MarkdownV2 test message failed to send.")

        print("\n--- Test 2: Sending message likely to fail MarkdownV2 (testing fallback) ---")
        # This message is intentionally not escaped to test the fallback mechanism.
        # The message_formatter.py currently produces messages like this.
        # For a real test, we'd use:
        # from message_formatter import format_message
        # price = 170.55
        # news = [{'title': 'Tesla Stock Up!', 'url': 'http://example.com/newsA'}]
        # unescaped_formatted_message = format_message(price, news) # This will have unescaped chars
        # For now, use a hardcoded string:
        unescaped_formatted_message = "Tesla (TSLA) Stock Price: $177.77\\n\\n--- Latest Tesla News ---\\n1. *Big News: Tesla's New Model!*\\n   http://example.com/new-model"

        success_unsafe = await send_telegram_message(unescaped_formatted_message)
        if success_unsafe:
            print("Potentially unescaped message sent/handled (check if plain text fallback was used).")
        else:
            print("Potentially unescaped message failed to send.")

    if config.TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN" and \
       config.TELEGRAM_BOT_TOKEN != "" and \
       config.TELEGRAM_CHAT_ID != "YOUR_TELEGRAM_CHAT_ID" and \
       config.TELEGRAM_CHAT_ID != "":
        asyncio.run(main_test())
    else:
        print("Please configure your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in config.py to test sending messages.")
        print("Skipping send_telegram_message test.")
