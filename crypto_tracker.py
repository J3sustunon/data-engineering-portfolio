"""
Cryptocurrency Price Tracker
Tracks real-time crypto prices using Coinbase API
No API key needed!
"""

import requests
import json
from datetime import datetime


def get_crypto_price(symbol):
    """
    Get current crypto price in USD
    
    Args:
        symbol (str): Crypto symbol (e.g., 'BTC', 'ETH', 'SOL')
    
    Returns:
        dict: Price data or None if request fails
    """
    
    url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        price = float(data['data']['amount'])
        
        # Format with commas for readability
        print(f"   {symbol:6} ${price:>12,.2f}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"   {symbol:6} Network error: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"   {symbol:6} Data error: {e}")
        return None


def get_crypto_details(symbol):
    """
    Get detailed crypto info including buy/sell prices
    
    Args:
        symbol (str): Crypto symbol
    
    Returns:
        dict: Detailed pricing data or None if request fails
    """
    
    try:
        # Spot price
        spot_url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        spot_response = requests.get(spot_url, timeout=10)
        spot_response.raise_for_status()
        spot_data = spot_response.json()
        
        # Buy price
        buy_url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/buy"
        buy_response = requests.get(buy_url, timeout=10)
        buy_response.raise_for_status()
        buy_data = buy_response.json()
        
        # Sell price
        sell_url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/sell"
        sell_response = requests.get(sell_url, timeout=10)
        sell_response.raise_for_status()
        sell_data = sell_response.json()
        
        spot_price = float(spot_data['data']['amount'])
        buy_price = float(buy_data['data']['amount'])
        sell_price = float(sell_data['data']['amount'])
        
        spread = buy_price - sell_price
        
        print(f"\n{symbol} DETAILED PRICING:")
        print(f"   Current Price: ${spot_price:,.2f}")
        print(f"   Buy Price:     ${buy_price:,.2f}")
        print(f"   Sell Price:    ${sell_price:,.2f}")
        print(f"   Spread:        ${spread:,.2f}")
        
        return {
            'spot': spot_price,
            'buy': buy_price,
            'sell': sell_price,
            'spread': spread
        }
        
    except requests.exceptions.RequestException as e:
        print(f"\nNetwork error getting {symbol} details: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"\nData error getting {symbol} details: {e}")
        return None


def main():
    """Main function"""
    
    print("\n" + "="*60)
    print(" "*18 + "CRYPTO PRICE TRACKER")
    print(" "*15 + datetime.now().strftime('%A, %B %d, %Y %I:%M %p'))
    print("="*60)
    
    # Major cryptocurrencies
    cryptos = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'MATIC']
    
    print("\nCURRENT PRICES:")
    print("-"*60)
    
    for crypto in cryptos:
        get_crypto_price(crypto)
    
    print("\n" + "="*60)
    
    # Get detailed info for Bitcoin
    get_crypto_details('BTC')
    
    # Save all data to file
    all_data = {}
    for crypto in cryptos:
        url = f"https://api.coinbase.com/v2/prices/{crypto}-USD/spot"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            all_data[crypto] = response.json()
        except requests.exceptions.RequestException:
            pass
    
    filename = f"crypto_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nSaved all data to {filename}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()