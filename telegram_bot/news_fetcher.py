from newsapi import NewsApiClient
import config

def get_tesla_news():
    """
    Fetches the latest news articles related to Tesla from NewsAPI.

    Returns:
        list: A list of dictionaries, where each dictionary contains the 
              'title' and 'url' of an article. Returns an empty list if 
              an error occurs or no articles are found.
    """
    try:
        newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
        
        # Fetch recent articles about Tesla
        all_articles = newsapi.get_everything(q='tesla',
                                              language='en',
                                              sort_by='publishedAt',
                                              page_size=5)
        
        articles_to_return = []
        if all_articles['status'] == 'ok':
            for article in all_articles['articles']:
                articles_to_return.append({
                    'title': article['title'],
                    'url': article['url']
                })
        return articles_to_return
    except Exception as e:
        print(f"Error fetching Tesla news: {e}")
        return []

if __name__ == '__main__':
    # For testing the function directly
    news_list = get_tesla_news()
    if news_list:
        print("Latest Tesla News:")
        for news_item in news_list:
            print(f"- {news_item['title']} ({news_item['url']})")
    else:
        print("Could not fetch Tesla news.")
