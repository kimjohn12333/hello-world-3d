import schedule
import time
import asyncio
import datetime
import pytz # For timezone handling

from stock_fetcher import get_tesla_stock_price
from news_fetcher import get_tesla_news
from message_formatter import format_message
from telegram_sender import send_telegram_message
import config

# Ensure essential config is set
if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or \
   not config.TELEGRAM_CHAT_ID or config.TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID" or \
   not config.ALPHA_VANTAGE_API_KEY or config.ALPHA_VANTAGE_API_KEY == "YOUR_ALPHA_VANTAGE_API_KEY" or \
   not config.NEWS_API_KEY or config.NEWS_API_KEY == "YOUR_NEWS_API_KEY":
    print("Essential API keys or Chat ID are not configured in config.py. Please set them up.")
    exit()

async def send_daily_update():
    print(f"[{datetime.datetime.now()}] Running daily update job...")
    # These functions are synchronous as per their current implementation.
    # If they were async, they would need to be awaited.
    print(f"[{datetime.datetime.now()}] Fetching Tesla stock price...")
    stock_price = get_tesla_stock_price() 
    
    print(f"[{datetime.datetime.now()}] Fetching Tesla news...")
    news_articles = get_tesla_news()
    
    print(f"[{datetime.datetime.now()}] Formatting message...")
    message = format_message(stock_price, news_articles)
    
    print(f"[{datetime.datetime.now()}] Attempting to send message...")
    success = await send_telegram_message(message) # This is async
    if success:
        print(f"[{datetime.datetime.now()}] Message sent successfully.")
    else:
        print(f"[{datetime.datetime.now()}] Failed to send message.")

def job_wrapper():
    current_time_utc = datetime.datetime.now(datetime.timezone.utc)
    kst_timezone = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time_utc.astimezone(kst_timezone)
    
    print(f"[{current_time_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}] Job wrapper called. KST time: [{current_time_kst.strftime('%Y-%m-%d %H:%M:%S %Z')}]")
    # It's better to create a new event loop for tasks run by a scheduler
    # if the scheduler itself isn't async-aware.
    asyncio.run(send_daily_update())

def get_schedule_time_utc_for_0630_kst():
    # KST is UTC+9. We want to schedule for 06:30 KST.
    # This means 21:30 UTC on the previous day.
    # The schedule library uses the server's local time for .at().
    # Assuming the server runs in UTC, we schedule for "21:30".
    return "21:30" 

if __name__ == "__main__":
    schedule_time_utc_str = get_schedule_time_utc_for_0630_kst()
    
    print(f"Bot started. Scheduling job daily at {schedule_time_utc_str} UTC (aiming for 06:30 KST).")
    print(f"Current server time (UTC): {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    kst_now = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone('Asia/Seoul'))
    print(f"Current KST time: {kst_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Schedule the job
    # If schedule_time_utc_str is "21:30", and server is UTC, this runs at 21:30 UTC.
    # This corresponds to 06:30 KST on the *next* KST calendar day.
    schedule.every().day.at(schedule_time_utc_str).do(job_wrapper)

    # Log the first scheduled run time more clearly
    next_run_server_time = schedule.next_run()
    if next_run_server_time:
        next_run_utc = pytz.utc.localize(next_run_server_time) # Assuming next_run() is naive UTC
        next_run_kst = next_run_utc.astimezone(pytz.timezone('Asia/Seoul'))
        print(f"Job scheduled. Next run at: {next_run_server_time.strftime('%Y-%m-%d %H:%M:%S')} (Server Time) / {next_run_kst.strftime('%Y-%m-%d %H:%M:%S %Z')} (KST)")
    else:
        print("Could not determine next run time.")


    print("Bot is running. Waiting for scheduled time or manual interruption...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60) # Check every minute
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Bot shutting down.")
