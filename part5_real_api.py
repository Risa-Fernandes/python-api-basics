"""
Part 5: Real-World APIs - Weather & Crypto Dashboard
====================================================
Difficulty: Advanced

Learn:
- Working with multiple real APIs
- Data formatting and presentation
- Building a simple CLI dashboard
- Using environment variables for API keys (optional)
"""

import requests, json, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# City coordinates (latitude, longitude)
CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "paris": (48.8566, 2.3522),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "toronto": (43.6532, -79.3832),
    "berlin": (52.5200, 13.4050),
    "moscow": (55.7558, 37.6173),
    "cape town": (-33.9249, 18.4241),
    "rio de janeiro": (-22.9068, -43.1729),
}

# Popular cryptocurrencies
CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
    "ripple": "xrp-xrp",
}


def get_weather(city_name):
    """
    Fetch weather data using Open-Meteo API (FREE, no API key needed).
    """
    city_lower = city_name.lower().strip()

    if city_lower not in CITIES:
        print(f"\nCity '{city_name}' not found.")
        print(f"Available cities: {', '.join(CITIES.keys())}")
        return None

    lat, lon = CITIES[city_lower]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None


def display_weather(city_name):
    """Display formatted weather information."""
    data = get_weather(city_name)

    if not data:
        return

    current = data["current_weather"]

    print(f"\n{'=' * 40}")
    print(f"  Weather in {city_name.title()}")
    print(f"{'=' * 40}")
    print(f"  Temperature: {current['temperature']}°C")
    print(f"  Wind Speed: {current['windspeed']} km/h")
    print(f"  Wind Direction: {current['winddirection']}°")

    # Weather condition codes
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        95: "Thunderstorm",
    }

    code = current.get("weathercode", 0)
    condition = weather_codes.get(code, "Unknown")
    print(f"  Condition: {condition}")
    print(f"{'=' * 40}")


def get_crypto_price(coin_name):
    """
    Fetch crypto data using CoinPaprika API (FREE, no API key needed).
    """
    coin_lower = coin_name.lower().strip()

    # Map common name to API ID
    coin_id = CRYPTO_IDS.get(coin_lower, coin_lower)

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching crypto data: {e}")
        return None


def display_crypto(coin_name):
    """Display formatted crypto information."""
    data = get_crypto_price(coin_name)

    if not data:
        print(f"\nCoin '{coin_name}' not found.")
        print(f"Available: {', '.join(CRYPTO_IDS.keys())}")
        return

    usd = data["quotes"]["USD"]

    print(f"\n{'=' * 40}")
    print(f"  {data['name']} ({data['symbol']})")
    print(f"{'=' * 40}")
    print(f"  Price: ${usd['price']:,.2f}")
    print(f"  Market Cap: ${usd['market_cap']:,.0f}")
    print(f"  24h Volume: ${usd['volume_24h']:,.0f}")
    print(f"  ")
    print(f"  1h Change:  {usd['percent_change_1h']:+.2f}%")
    print(f"  24h Change: {usd['percent_change_24h']:+.2f}%")
    print(f"  7d Change:  {usd['percent_change_7d']:+.2f}%")
    print(f"{'=' * 40}")


def compare_cryptos():
    """Compare prices of multiple cryptos entered by the user."""
    print("\n=== Crypto Price Comparison ===")
    print(f"Available: {', '.join(CRYPTO_IDS.keys())}")
    
    user_input = input("Enter coins to compare (comma-separated, e.g., bitcoin, ethereum, solana): ")
    coin_list = [c.strip().lower() for c in user_input.split(",")]

    # Table Header
    print(f"\n{'=' * 65}")
    print(f"{'Coin Name':<15}{'Price (USD)':>15}{'24h Change':>15}{'Market Cap':>18}")
    print(f"{'-' * 65}")

    for coin in coin_list:
        data = get_crypto_price(coin)
        
        if data:
            usd = data["quotes"]["USD"]
            name = data["name"]
            price = f"${usd['price']:,.2f}"
            change = f"{usd['percent_change_24h']:+.2f}%"
            mkt_cap = f"${usd['market_cap'] / 1_000_000_000:,.1f}B" # Display in Billions

            # Print formatted row
            print(f"{name:<15}{price:>15}{change:>15}{mkt_cap:>18}")
        else:
            print(f"{coin.title():<15} [!] Data Not Found")

    print(f"{'=' * 65}")


def get_top_cryptos(limit=5):
    """Fetch top cryptocurrencies by market cap."""
    url = "https://api.coinpaprika.com/v1/tickers"
    params = {"limit": limit}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def display_top_cryptos():
    """Display top 5 cryptocurrencies."""
    data = get_top_cryptos(5)

    if not data:
        return

    print(f"\n{'=' * 55}")
    print(f"  Top 5 Cryptocurrencies by Market Cap")
    print(f"{'=' * 55}")
    print(f"  {'Rank':<6}{'Name':<15}{'Price':<15}{'24h Change'}")
    print(f"  {'-' * 50}")

    for coin in data:
        usd = coin["quotes"]["USD"]
        change = usd["percent_change_24h"]
        change_str = f"{change:+.2f}%"

        print(f"  {coin['rank']:<6}{coin['name']:<15}${usd['price']:>12,.2f}  {change_str}")

    print(f"{'=' * 55}")


def create_post():
    """Simulate creating a new post using a POST request."""
    print("\n=== Create New Post (Simulation) ===")
    
    title = input("Enter post title: ")
    body = input("Enter post content: ")
    user_id = input("Enter your User ID: ")

    url = "https://jsonplaceholder.typicode.com/posts"
    
    # The data we are sending to the server
    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    try:
        # We use .post() and the 'json' parameter
        response = requests.post(url, json=payload, timeout=10)
        
        # HTTP 201 means "Created"
        if response.status_code == 201:
            new_post = response.json()
            print(f"\n✅ Success! Post created on the server.")
            print(f"Server Assigned ID: {new_post['id']}")
            print(f"Title: {new_post['title']}")
        else:
            print(f"Failed to create post. Status code: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")



def save_to_file(data, filename="results.json"):
    """Saves any dictionary data to a JSON file."""
    try:
        with open(filename, "w") as f:
            # indent=4 makes the file human-readable (pretty-print)
            json.dump(data, f, indent=4)
        print(f"\n📂 Data successfully saved to {filename}!")
    except Exception as e:
        print(f"Error saving file: {e}")

def get_and_save_weather():
    """Fetch weather and save it immediately."""
    city = input("Enter city to save weather for: ").strip().lower()
    data = get_weather(city)
    
    if data:
        # Add a timestamp to the data so we know when it was saved
        data['saved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_to_file(data, f"{city}_weather.json")



def get_openweathermap(city_name):
    """Fetch current weather using OpenWeatherMap (Requires API Key)."""
    
    # 1. Retrieve the secret key from environment variables
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("\n[!] Error: API Key not found!")
        print("Please set the 'OPENWEATHER_API_KEY' environment variable.")
        return None

    # 2. Build the request
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Converts temperature to Celsius
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        
        # If the key is invalid or city doesn't exist, this raises an error
        response.raise_for_status() 
        
        data = response.json()
        
        # 3. Format and display the results
        print(f"\n{'=' * 40}")
        print(f"   OpenWeatherMap: {data['name']}, {data['sys']['country']}")
        print(f"{'=' * 40}")
        print(f"   Temperature: {data['main']['temp']}°C")
        print(f"   Humidity:    {data['main']['humidity']}%")
        print(f"   Description: {data['weather'][0]['description'].capitalize()}")
        print(f"{'=' * 40}")
        
        return data

    except requests.exceptions.HTTPError:
        print(f"\n[!] City '{city_name}' not found or API Key is invalid.")
    except Exception as e:
        print(f"\n[!] Connection Error: {e}")
    return None


def dashboard():
    """Interactive dashboard combining weather and crypto."""
    print("\n" + "=" * 50)
    print("   Real-World API Dashboard")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("  1. Check Weather")
        print("  2. Check Crypto Price")
        print("  3. View Top 5 Cryptos")
        print("  4. Quick Dashboard (Delhi + Bitcoin)")
        print("  5. Compare Multiple Cryptos")
        print("  6. Create a New Post")
        print("  7. Save file")
        print("  8. Advanced Weather (OpenWeatherMap)")
        print("  9. Exit")

        choice = input("\nSelect (1-5): ").strip()

        if choice == "1":
            print(f"\nAvailable: {', '.join(CITIES.keys())}")
            city = input("Enter city name: ")
            display_weather(city)

        elif choice == "2":
            print(f"\nAvailable: {', '.join(CRYPTO_IDS.keys())}")
            coin = input("Enter crypto name: ")
            display_crypto(coin)

        elif choice == "3":
            display_top_cryptos()

        elif choice == "4":
            display_weather("delhi")
            display_crypto("bitcoin")

        elif choice == "5":
            compare_cryptos() 

        elif choice == "6": 
            create_post()
        
        elif choice == "7":
            city = input("Enter city to save weather for: ")
            data = get_weather(city) # 1. Fetch the data first
            if data:
                save_to_file(data)   # 2. Pass that data into the function           

        elif choice == "8": 
            get_openweathermap(input("Enter city: "))

        elif choice == "9":
            print("\nGoodbye! Happy coding!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    dashboard()


# --- CHALLENGE EXERCISES ---
#
# Exercise 1: Add more cities to the CITIES dictionary
#             Find coordinates at: https://www.latlong.net/
#
# Exercise 2: Create a function that compares prices of multiple cryptos
#             Display them in a formatted table
#
# Exercise 3: Add POST request example
#             Use: https://jsonplaceholder.typicode.com/posts
#             Send: requests.post(url, json={"title": "My Post", "body": "Content"})
#
# Exercise 4: Save results to a JSON file
#             import json
#             with open("results.json", "w") as f:
#                 json.dump(data, f, indent=2)
#
# Exercise 5: Add API key support for OpenWeatherMap
#             Sign up at: https://openweathermap.org/api
#             Use environment variables:
#             import os
#             api_key = os.environ.get("OPENWEATHER_API_KEY")
