# Student Name: Sandeep Reddy Seernam
# Student ID: @101470173
# Student Email ID: sseernam@fitchburgstate.edu

import datetime
import requests
import json
import os
import sqlite3

# --------------------------
# API Configuration
# --------------------------
API_KEY = "00fa39c06f71611fb5a46d08cfbce5b0"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
HISTORY_FILE = "aqi_history.json"
DB_FILE = "skyscan.db"

AQI_MESSAGES = {
    1: "Good air quality — safe for everyone.",
    2: "Fair — acceptable, but sensitive individuals should be cautious.",
    3: "Moderate — sensitive groups may experience health effects.",
    4: "Poor — everyone may experience health effects.",
    5: "Very Poor — health alert! Avoid outdoor activity."
}


# --------------------------
# Database Functions
# --------------------------

def init_db():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aqi_searches (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            city    TEXT    NOT NULL,
            country TEXT,
            lat     REAL,
            lon     REAL,
            aqi     INTEGER,
            message TEXT,
            time    TEXT
        )
    """)
    # Reset ID counter so it always starts from 1 on fresh runs
    cursor.execute("DELETE FROM aqi_searches")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='aqi_searches'")
    conn.commit()
    conn.close()
    print(f"[DB] Database '{DB_FILE}' initialized successfully.")

def save_to_db(city, country, lat, lon, aqi, message):
    """Inserts one search record into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aqi_searches (city, country, lat, lon, aqi, message, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        city.title(),
        country,
        lat,
        lon,
        aqi,
        message,
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
    print("[DB] Record saved to database successfully.")


def show_db_history():
    """Reads and prints all records from the database — demonstrates a successful DB read call."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, city, country, aqi, message, time FROM aqi_searches ORDER BY time DESC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("[DB] No records found in database.")
        return

    print("\n" + "=" * 60)
    print(f"{'ID':<5} {'City':<15} {'Country':<10} {'AQI':<5} {'Time':<20}")
    print("=" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<10} {row[3]:<5} {row[5]:<20}")
        print(f"      {row[4]}")
        print("-" * 60)


# --------------------------
# Existing Functions (unchanged)
# --------------------------

def validate_city_input(user_input):
    clean_input = user_input.strip()
    if not clean_input:
        return False, "Input cannot be empty."
    if clean_input.isdigit():
        return False, f"'{clean_input}' is not a valid city name (numbers only)."
    if len(clean_input) < 2:
        return False, "City name is too short (minimum 2 characters)."
    return True, None


def get_coordinates(city_name):
    params = {"q": city_name, "appid": API_KEY, "limit": 5}
    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None, None, None, None

        for place in data:
            if place["name"].lower() == city_name.lower():
                lat = place["lat"]
                lon = place["lon"]
                country = place.get("country", "Unknown")
                state = place.get("state", "")
                return lat, lon, country, state

        print(f"Notice: No exact match found for '{city_name}'.")
        return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"\n[CONNECTION ERROR]: {e}")
        return None, None, None, None


def fetch_air_quality(lat, lon):
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    response = requests.get(AIR_POLLUTION_URL, params=params)
    response.raise_for_status()
    return response.json()["list"][0]["main"]["aqi"]


def save_history(city, aqi, lat, lon, country):
    record = {
        "city": city.title(),
        "country": country,
        "lat": lat,
        "lon": lon,
        "aqi": aqi,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
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
# Main Program Loop
# --------------------------

def run_skyscan():
    print("--- SkyScan: Exact Match Mode ---")
    init_db()  # Initialize database on startup

    while True:
        user_input = input("\nEnter City Name (or 'exit' / 'history'): ").strip()

        if user_input.lower() == "exit":
            break

        # NEW: show database history on demand
        if user_input.lower() == "history":
            show_db_history()
            continue

        valid, msg = validate_city_input(user_input)
        if not valid:
            print(f"Validation Error: {msg}")
            continue

        lat, lon, country, state = get_coordinates(user_input)

        if lat is None:
            continue

        location_str = f"{user_input.title()}, {state}, {country}" if state else f"{user_input.title()}, {country}"
        print("-" * 40)
        print(f"EXACT MATCH FOUND: {location_str}")
        print(f"LATITUDE:  {lat}")
        print(f"LONGITUDE: {lon}")
        print("-" * 40)

        try:
            aqi = fetch_air_quality(lat, lon)
            message = AQI_MESSAGES.get(aqi, "No data.")
            print(f"Air Quality Index: {aqi} ({message})")

            # Save to both JSON (original) and SQLite database (new)
            save_history(user_input, aqi, lat, lon, country)
            save_to_db(user_input, country, lat, lon, aqi, message)
            print("Successfully saved to history.")

        except Exception as e:
            print(f"Error fetching AQI: {e}")


if __name__ == "__main__":
    run_skyscan()