def format_message(stock_price, news_articles):
    message_parts = []

    # Add stock price information
    if stock_price is not None:
        message_parts.append(f"Tesla (TSLA) Stock Price: ${stock_price:.2f}")
    else:
        message_parts.append("Could not retrieve Tesla stock price at this time.")
    
    # This string should contain literal \n for Telegram
    message_parts.append("\\n--- Latest Tesla News ---")

    # Add news articles
    if news_articles:
        for i, article in enumerate(news_articles, 1):
            # This string should contain literal \n for Telegram
            message_parts.append(f"{i}. *{article['title']}*\\n   {article['url']}")
    else:
        message_parts.append("No relevant Tesla news found at this time.")
        
    # The join string should also be a literal \n\n for Telegram
    return "\\n\\n".join(message_parts)

if __name__ == '__main__':
    # Example Usage for testing
    sample_price_ok = 175.23
    sample_price_fail = None
    
    sample_news_ok = [
        {'title': 'Tesla Article 1: The Future of EVs', 'url': 'http://example.com/news1'},
        {'title': 'Tesla Article 2: Stock Analysis', 'url': 'http://example.com/news2'},
        {'title': 'Tesla Article 3: Giga Factory Updates', 'url': 'http://example.com/news3'}
    ]
    sample_news_empty = []
    sample_news_none = None

    # When printing to console for testing, we can replace "\n" with actual newlines
    # to see a more representative output.
    print("--- Test Case 1: Price OK, News OK ---")
    print(format_message(sample_price_ok, sample_news_ok).replace("\\n", "\n")) 
    
    print("\\n\\n--- Test Case 2: Price Fail, News OK ---")
    print(format_message(sample_price_fail, sample_news_ok).replace("\\n", "\n"))
    
    print("\\n\\n--- Test Case 3: Price OK, News Empty ---")
    print(format_message(sample_price_ok, sample_news_empty).replace("\\n", "\n"))
    
    print("\\n\\n--- Test Case 4: Price OK, News None ---")
    print(format_message(sample_price_ok, sample_news_none).replace("\\n", "\n"))
    
    print("\\n\\n--- Test Case 5: All Fail/None (Price None, News None) ---")
    print(format_message(None, None).replace("\\n", "\n"))

    print("\\n\\n--- Test Case 6: Price Fail, News Empty ---")
    print(format_message(sample_price_fail, sample_news_empty).replace("\\n", "\n"))
