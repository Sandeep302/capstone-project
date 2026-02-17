#Assignment 2
# Student Name: Sandeep Reddy Seernam
#Student ID:@101470173
# Student Email ID:sseernam@fitchburgstate.edu
#


import datetime
import requests
import json
import os

# --------------------------
# API Configuration
# --------------------------
API_KEY = "00fa39c06f71611fb5a46d08cfbce5b0"  # Replace with your OpenWeatherMap API key
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
HISTORY_FILE = "aqi_history.json"

# Constants for AQI interpretation
AQI_MESSAGES = {
    1: "Good air quality — safe for everyone.",
    2: "Fair — acceptable, but sensitive individuals should be cautious.",
    3: "Moderate — sensitive groups may experience health effects.",
    4: "Poor — everyone may experience health effects.",
    5: "Very Poor — health alert! Avoid outdoor activity."
}

# --------------------------
# Functions
# --------------------------
def get_current_time():
    """Return formatted current time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_coordinates(city_name):
    """Convert city name to latitude and longitude using OWM Geocoding API."""
    params = {"q": city_name, "appid": API_KEY, "limit": 1}
    response = requests.get(GEOCODE_URL, params=params).json()
    if response:
        return response[0]["lat"], response[0]["lon"]
    return None, None

def fetch_air_quality(lat, lon):
    """Fetch AQI data using OpenWeatherMap Air Pollution API."""
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    response = requests.get(AIR_POLLUTION_URL, params=params).json()
    return response["list"][0]["main"]["aqi"]

def interpret_aqi(aqi):
    """Convert AQI number to a readable health message."""
    return AQI_MESSAGES.get(aqi, "Unknown AQI level.")

def save_history(city, aqi):
    """Save AQI results to a local JSON history file."""
    record = {"city": city, "aqi": aqi, "time": get_current_time()}
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    history.append(record)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# --------------------------
# Main Program: SkyScan
# --------------------------
def run_skyscan_init():
    # Initialization and timestamp
    current_time = get_current_time()
    print(f"--- SkyScan Live System Initialization ---")
    print(f"Current System Time: {current_time}")
    print("Status: Network protocols ready.")

    while True:
        city = input("\nEnter a city (or 'test'/'exit'): ").strip()

        if city.lower() == "exit":
            print("\nExiting SkyScan. Goodbye!")
            break
        elif city.lower() == "test":
            print(f"\n[SUCCESS] Environment check passed.")
            print("Ready to implement OpenWeatherMap API integration.")
        elif city == "":
            print("Error: No city entered. Try again.")
        else:
            # Get coordinates and AQI
            lat, lon = get_coordinates(city)
            if lat is None:
                print("Could not find location. Try another city.")
                continue
            try:
                aqi = fetch_air_quality(lat, lon)
                message = interpret_aqi(aqi)
                print(f"\nAir Quality in {city.title()}: {aqi} — {message}")
                save_history(city.title(), aqi)
                print(f"History saved for {city.title()}.")
            except Exception as e:
                print("Error fetching air quality data:", e)

# --------------------------
# Entry Point
# --------------------------
# --------------------------
# Entry Point
# --------------------------
if __name__ == "__main__":
    run_skyscan_init()
