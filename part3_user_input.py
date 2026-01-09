"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate

Learn:
- Using input() to make dynamic API requests
- Building URLs with f-strings
- Query parameters in URLs
"""

import requests



def get_valid_id(prompt, min_val=1, max_val=10):
    """
    Prompts user for an ID and validates that it is a number 
    within the specified range.
    """
    while True:
        user_input = input(prompt).strip()
        
        # 1. Check if the input is actually a number
        if not user_input.isdigit():
            print(f"Error: '{user_input}' is not a number. Please enter a digit.")
            continue
        
        # 2. Convert to integer and check the range
        val = int(user_input)
        if min_val <= val <= max_val:
            return str(val) # Return as string for the URL f-string
        else:
            print(f"Error: Please enter a number between {min_val} and {max_val}.")



def get_user_info():
    user_id = input("Enter user ID (1-10): ")
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    
    try:
        response = requests.get(url, timeout=5) # Added a timeout
        if response.status_code == 200:
            data = response.json()
            print(f"\n--- User #{user_id} Info ---")
            print(f"Name: {data['name']}")
            # ... rest of prints
        else:
            print(f"Error: Server returned status {response.status_code}")
    except Exception as e:
        print(f"Connection Error: {e}")


def search_posts():
    """Search posts by user ID."""
    print("\n=== Post Search ===\n")

    user_id = input("Enter user ID to see their posts (1-10): ")

    # Using query parameters
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": user_id}

    response = requests.get(url, params=params)
    posts = response.json()

    if posts:
        print(f"\n--- Posts by User #{user_id} ---")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
    else:
        print("No posts found for this user.")


def get_crypto_price():
    """Fetch cryptocurrency price based on user input."""
    print("\n=== Cryptocurrency Price Checker ===\n")

    print("Available coins: btc-bitcoin, eth-ethereum, doge-dogecoin")
    coin_id = input("Enter coin ID (e.g., btc-bitcoin): ").lower().strip()

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price_usd = data['quotes']['USD']['price']
        change_24h = data['quotes']['USD']['percent_change_24h']

        print(f"\n--- {data['name']} ({data['symbol']}) ---")
        print(f"Price: ${price_usd:,.2f}")
        print(f"24h Change: {change_24h:+.2f}%")
    else:
        print(f"\nCoin '{coin_id}' not found!")
        print("Try: btc-bitcoin, eth-ethereum, doge-dogecoin")



def get_coordinates(city_name):
    """
    Helper function to convert city name to lat/long using Open-Meteo's Geocoding API.
    """
    # Open-Meteo provides a free geocoding endpoint
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    
    response = requests.get(geo_url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            # Return the first match
            return results[0]['latitude'], results[0]['longitude'], results[0]['name']
    return None, None, None

def get_weather_info():
    """Fetch weather info based on user input city."""
    print("\n=== Weather Information Lookup ===")
    
    city_input = input("Enter city name (e.g., Delhi, Tokyo, New York): ").strip()
    
    # Step 1: Get coordinates for the city
    lat, lon, official_name = get_coordinates(city_input)
    
    if lat is None:
        print(f"Could not find coordinates for '{city_input}'.")
        return

    # Step 2: Use coordinates to get weather
    # We use f-strings to insert the dynamic lat and lon
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    response = requests.get(weather_url)
    
    if response.status_code == 200:
        data = response.json()
        current = data['current_weather']
        
        print(f"\n--- Weather in {official_name} ---")
        print(f"Latitude:  {lat}")
        print(f"Longitude: {lon}")
        print(f"Temperature: {current['temperature']}°C")
        print(f"Wind Speed:  {current['windspeed']} km/h")
    else:
        print(f"\nError fetching weather data for {official_name}.")


def search_todos():
    """Search todos based on completion status."""
    print("\n=== Todo List Filter ===")
    
    choice = input("View completed tasks? (y/n): ").lower().strip()
    
    # Map user input to API expected values
    if choice == 'y':
        status = "true"
    elif choice == 'n':
        status = "false"
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        return

    # Using query parameters to filter the list
    url = "https://jsonplaceholder.typicode.com/todos"
    params = {"completed": status}

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        todos = response.json()
        # Limiting to first 10 for readability
        print(f"\n--- Showing {len(todos[:10])} tasks (Status: Completed={status}) ---")
        for todo in todos[:10]:
            mark = "[✓]" if todo['completed'] else "[ ]"
            print(f"{mark} {todo['title']}")
    else:
        print("Failed to retrieve todos.")

def main():
    """Main menu for the program."""
    print("=" * 40)
    print("   Dynamic API Query Demo")
    print("=" * 40)

    while True:
        print("\nChoose an option:")
        print("1. Look up user info")
        print("2. Search posts by user")
        print("3. Check crypto price")
        print("4. Get Weather Info")
        print("5. Filter Todos")
        print("6. Exit")

        choice = input("\nEnter choice (1-5): ")

        if choice == "1":
            get_user_info()
        elif choice == "2":
            search_posts()
        elif choice == "3":
            get_crypto_price()
        elif choice == "4":
            get_weather_info()
        elif choice == "5":
            search_todos()
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# --- EXERCISES ---
#
# Exercise 1: Add a function to fetch weather for a city
#             Use Open-Meteo API (no key required):
#             https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.23&current_weather=true
#             Challenge: Let user input city name (you'll need to find lat/long)
#
# Exercise 2: Add a function to search todos by completion status
#             URL: https://jsonplaceholder.typicode.com/todos
#             Params: completed=true or completed=false
#
# Exercise 3: Add input validation (check if user_id is a number)
