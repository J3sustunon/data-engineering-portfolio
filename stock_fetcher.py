"""
Stock Data Fetcher
Fetches real-time stock data from Alpha Vantage API
"""

import requests
import json
from datetime import datetime

def fetch_stock_data(symbol, api_key):
    """
    Fetch stock data for a given symbol
    
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        api_key (str): Alpha Vantage API key
    
    Returns:
        dict: Stock data from API
    """
    
    # Build the API URL
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    
    print(f"Fetching data for {symbol}...")
    
    try:
        # Make the request
        response = requests.get(url)
        data = response.json()
        
        # Check if we got data
        if "Time Series (5min)" in data:
            num_points = len(data["Time Series (5min)"])
            print(f"Success! Received {num_points} data points")
            
            # Save to JSON file
            filename = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Saved to {filename}")
            return data
            
        else:
            print("Error: No data received")
            print(f"Response: {data}")
            return None
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def main():
    """Main function to run the script"""
    
    # YOUR API KEY HERE - paste your actual Alpha Vantage key
    API_KEY = "55DM4UT1W8LSDM59"
    
    # Stock symbol to fetch
    symbol = "AAPL"
    
    print("="*50)
    print("Stock Data Fetcher")
    print("="*50)
    
    # Fetch the data
    data = fetch_stock_data(symbol, API_KEY)
    
    if data and "Time Series (5min)" in data:
        # Show the most recent price
        time_series = data["Time Series (5min)"]
        latest_time = list(time_series.keys())[0]
        latest_price = time_series[latest_time]["1. open"]
        
        print(f"\n📈 Latest {symbol} price: ${latest_price}")
        print(f"⏰ Time: {latest_time}")
    
    print("="*50)


# This runs when you execute the script
if __name__ == "__main__":
    main()
