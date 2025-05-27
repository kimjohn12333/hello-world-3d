from alpha_vantage.timeseries import TimeSeries
import config

def get_tesla_stock_price():
    """
    Fetches the latest intraday stock price for Tesla (TSLA) from Alpha Vantage.

    Returns:
        float: The latest closing price of TSLA, or None if an error occurs.
    """
    try:
        ts = TimeSeries(key=config.ALPHA_VANTAGE_API_KEY, output_format='json')
        # Fetch intraday data for TSLA
        # Note: Alpha Vantage API might return data in an OrderedDict-like structure,
        # so the first key is usually the latest for compact output.
        data, meta_data = ts.get_intraday(symbol='TSLA', interval='1min', outputsize='compact')
        
        # Get the latest timestamp (first key in the ordered dict from json response)
        # The keys are strings like '2024-05-28 15:59:00'
        latest_timestamp = list(data.keys())[0]
        latest_price = float(data[latest_timestamp]['4. close'])
        return latest_price
    except Exception as e:
        print(f"Error fetching Tesla stock price: {e}")
        return None

if __name__ == '__main__':
    # For testing the function directly
    price = get_tesla_stock_price()
    if price is not None:
        print(f"Tesla Stock Price: ${price:.2f}")
    else:
        print("Could not fetch Tesla stock price.")
