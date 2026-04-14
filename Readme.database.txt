# SkyScan Live

**A real-time CLI dashboard that fetches and displays weather metrics and Air Quality Index (AQI) for any user-specified city.**

---

## Project Goal

Connect to live weather and air quality APIs to give users instant, accurate environmental data for any city — with full search history stored locally for future analysis.

---

## Core Features (MVP)

- Connect to a weather API to retrieve live temperature data
- Simple CLI interface to input city names
- Display basic "Feels Like" and humidity levels
- Real-time AQI lookup with human-readable health guidance
- Input validation to catch empty, numeric, or too-short city names

---

## New in This Version

- **SQLite database integration** — every search is now permanently stored in a local `skyscan.db` database

---

## Database Selection & Reasoning

### Chosen Database: SQLite (via Python's built-in `sqlite3` module)

For this project, **SQLite** was selected as the data storage solution for the following reasons:

- **Zero setup, fully free** — SQLite requires no server installation, no account, and no configuration. It ships with Python's standard library, meaning no extra dependencies are needed.
- **Right-sized for the project** — SkyScan is a single-user CLI tool. A full client-server database like PostgreSQL or MySQL would be significant overkill for storing AQI search records locally.
- **Persistent and queryable** — Unlike a plain JSON file, SQLite stores data in a structured, queryable format. This makes it easy to sort, filter, or expand the history feature in the future.
- **Supports the "Future Features" roadmap** — The original project plan called for saving daily snapshots for historical analysis. SQLite is a natural fit for that goal and can be swapped for a larger database later if needed without changing the application logic.
- **Aligns with the free-tier requirement** — The entire database runs as a single `.db` file on disk with no cost, no rate limits, and no internet dependency.


### Example Successful Database Call

```
Enter City Name (or 'exit' / 'history'): Boston
----------------------------------------
EXACT MATCH FOUND: Boston, Massachusetts, US
LATITUDE:  42.3554334
LONGITUDE: -71.060511
----------------------------------------
Air Quality Index: 2 (Fair — acceptable, but sensitive individuals should be cautious.)
[DB] Record saved to database successfully.
Successfully saved to history.
```

Typing `history` then returns:

```
============================================================
ID    City            Country    AQI   Time
============================================================
1     Boston          US         2     2025-06-10 14:32:01
      Fair — acceptable, but sensitive individuals should be cautious.
------------------------------------------------------------
```
---

## Database Schema

```sql
CREATE TABLE aqi_searches (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    city    TEXT    NOT NULL,
    country TEXT,
    lat     REAL,
    lon     REAL,
    aqi     INTEGER,
    message TEXT,
    time    TEXT
);
```

> **Note:** The database resets each time the application starts. To retain history across sessions, remove the `DELETE` statements inside the `init_db()` function.

---

## Future Features

- **Real-time Alerts** — Desktop notifications for severe weather or high AQI warnings
- **Historical Analysis** — Query the SQLite database to chart AQI trends over time for a city
- **GUI Upgrade** — Move from CLI to a web dashboard using Streamlit
- **Cloud Database** — Migrate from local SQLite to a hosted database (e.g., Supabase free tier) to enable multi-device access

---

## Author

- **Name:** Sandeep Reddy Seernam
- **Student ID:** 101470173
- **Email:** sseernam@fitchburgstate.edu
