"""
Weather Data Fetcher
Fetches current weather for any city using wttr.in API
No API key needed!
"""

import requests
import json
from datetime import datetime

def get_weather(city):
    """
    Get current weather for a city
    
    Args:
        city (str): City name (e.g., 'Miami', 'New York')
    
    Returns:
        dict: Weather data
    """
    
    # API endpoint - returns JSON format
    url = f"https://wttr.in/{city}?format=j1"
    
    print(f"\nFetching weather for {city}...")
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extract current conditions
        current = data['current_condition'][0]
        location = data['nearest_area'][0]
        
        # Display weather info
        print(f"Location: {location['areaName'][0]['value']}, {location['country'][0]['value']}")
        print(f"Temperature: {current['temp_F']}°F (Feels like {current['FeelsLikeF']}°F)")
        print(f"Conditions: {current['weatherDesc'][0]['value']}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind: {current['windspeedMiles']} mph {current['winddir16Point']}")
        print(f"Visibility: {current['visibility']} miles")
        
        # Save to file
        filename = f"weather_{city.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved to {filename}")
        
        return data
        
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    """Main function"""
    
    print("="*60)
    print(" "*20 + "WEATHER FETCHER")
    print(" "*15 + datetime.now().strftime('%A, %B %d, %Y'))
    print("="*60)
    
    # Get weather for multiple cities
    cities = ["Miami", "New York", "San Francisco"]
    
    for city in cities:
        get_weather(city)
        print("\n" + "-"*60)
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()