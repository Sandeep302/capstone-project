# Student Name: Sandeep Reddy Seernam
#Student ID:@101470173
# Student Email ID:sseernam@fitchburgstate.edu

import datetime  # Import module to get the current date and time
import requests  # Import module to send network requests to the API
import json  # Import module to handle JSON data format
import os  # Import module to check if files exist on the computer

# --------------------------
# API Configuration
# --------------------------
API_KEY = "00fa39c06f71611fb5a46d08cfbce5b0"  # Your unique OpenWeatherMap API key
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"  # URL to convert City Name -> Lat/Long
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"  # URL to get Air Quality
HISTORY_FILE = "aqi_history.json"  # Name of the local file where data is saved

# Mapping AQI numbers (1-5) to human-readable health advice strings
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

def validate_city_input(user_input):  # Function to check if user input is valid
    """Validates basic string properties before API call."""
    clean_input = user_input.strip()  # Remove leading/trailing whitespace
    if not clean_input:  # If the string is empty after stripping
        return False, "Input cannot be empty."  # Return failure and message
    if clean_input.isdigit():  # If the user typed only numbers (e.g., '123')
        return False, f"'{clean_input}' is not a valid city name (numbers only)."  # Return failure
    if len(clean_input) < 2:  # If name is only 1 letter (e.g., 'a')
        return False, "City name is too short (minimum 2 characters)."  # Return failure
    return True, None  # If all checks pass, return True and no error message


def get_coordinates(city_name):  # Function to fetch Lat/Long from city name
    """Fetches coordinates and ensures an EXACT name match."""
    # Define parameters for the API: search query, key, and limit results to 5
    params = {"q": city_name, "appid": API_KEY, "limit": 5}
    try:  # Start error handling block for network requests
        response = requests.get(GEOCODE_URL, params=params, timeout=5)  # Send GET request with 5s timeout
        response.raise_for_status()  # Check if the HTTP request was successful (200 OK)
        data = response.json()  # Convert the raw response into a Python list/dictionary

        if not data:  # If the list is empty, the API found nothing
            return None, None, None, None  # Return empty values

        # Loop through up to 5 results to find a name that matches exactly
        for place in data:  # Iterate through each location found by the API
            if place["name"].lower() == city_name.lower():  # Check for case-insensitive exact match
                lat = place["lat"]  # Extract the Latitude
                lon = place["lon"]  # Extract the Longitude
                country = place.get("country", "Unknown")  # Get Country code, default to 'Unknown'
                state = place.get("state", "")  # Get State name if available
                return lat, lon, country, state  # Return the successful data

        # If no exact match was found among the 5 results
        print(f"Notice: No exact match found for '{city_name}'.")  # Print warning
        return None, None, None, None  # Return empty values

    except requests.exceptions.RequestException as e:  # Catch network errors (like no Wi-Fi)
        print(f"\n[CONNECTION ERROR]: {e}")  # Print the specific error message
        return None, None, None, None  # Return empty values


def fetch_air_quality(lat, lon):  # Function to get AQI using coordinates
    """Retrieves AQI index for specific coordinates."""
    params = {"lat": lat, "lon": lon, "appid": API_KEY}  # Setup API parameters
    response = requests.get(AIR_POLLUTION_URL, params=params)  # Send request to Air Pollution API
    response.raise_for_status()  # Ensure request was successful
    return response.json()["list"][0]["main"]["aqi"]  # Return the specific AQI integer


def save_history(city, aqi, lat, lon, country):  # Function to log data to JSON file
    """Logs the full result to a local JSON file."""
    record = {  # Create a dictionary representing one search entry
        "city": city.title(),  # Capitalize city name
        "country": country,  # Store country code
        "lat": lat,  # Store Latitude
        "lon": lon,  # Store Longitude
        "aqi": aqi,  # Store AQI value
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date/time string
    }
    history = []  # Initialize empty list for history
    if os.path.exists(HISTORY_FILE):  # If the JSON file already exists on disk
        with open(HISTORY_FILE, "r") as f:  # Open the file in read mode
            try:  # Handle cases where the file might be broken/empty
                history = json.load(f)  # Load existing list of records
            except json.JSONDecodeError:  # If JSON is corrupted
                history = []  # Reset to empty list
    history.append(record)  # Add the new record to the list
    with open(HISTORY_FILE, "w") as f:  # Open file in write mode
        json.dump(history, f, indent=4)  # Save the list back to file with pretty formatting


# --------------------------
# Main Program Loop
# --------------------------

def run_skyscan():  # Main function to run the application logic
    print("--- SkyScan: Exact Match Mode ---")  # Display program header

    while True:  # Start an infinite loop for user interaction
        user_input = input("\nEnter City Name (or 'exit'): ").strip()  # Ask user for city

        if user_input.lower() == "exit":  # If user types 'exit' (any case)
            break  # Stop the infinite loop

        # 1. VALIDATION: Check if input format is correct
        valid, msg = validate_city_input(user_input)  # Call validation function
        if not valid:  # If input failed validation
            print(f"Validation Error: {msg}")  # Show why it failed
            continue  # Go back to the start of the loop

        # 2. COORDINATES: Call API to get Lat/Long and Country
        lat, lon, country, state = get_coordinates(user_input)  # Unpack returned values

        if lat is None:  # If no exact city match was found in the API search
            continue  # Skip to next input

        # 3. OUTPUT: Show the precise location data found
        # Build location string: City, State, Country (hides state if empty)
        location_str = f"{user_input.title()}, {state}, {country}" if state else f"{user_input.title()}, {country}"
        print("-" * 40)  # Visual separator line
        print(f"EXACT MATCH FOUND: {location_str}")  # Show full location name
        print(f"LATITUDE:  {lat}")  # Display Latitude in terminal
        print(f"LONGITUDE: {lon}")  # Display Longitude in terminal
        print("-" * 40)  # Visual separator line

        # 4. AIR QUALITY: Get AQI using the validated coordinates
        try:  # Try block for air quality data fetching
            aqi = fetch_air_quality(lat, lon)  # Get AQI number
            message = AQI_MESSAGES.get(aqi, "No data.")  # Get message from dictionary
            print(f"Air Quality Index: {aqi} ({message})")  # Display AQI and advice

            # 5. SAVE: Record the search in the history file
            save_history(user_input, aqi, lat, lon, country)  # Call save function
            print("Successfully saved to history.")  # Confirm save
        except Exception as e:  # Catch any unexpected errors during AQI fetch
            print(f"Error fetching AQI: {e}")  # Show the error


if __name__ == "__main__":  # Boilerplate to ensure script runs correctly
    run_skyscan()  # Call the main run function