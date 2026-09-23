

import sqlite3

connection = sqlite3.connect("swim_results.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE meets (
        meet_id INTEGER PRIMARY KEY,
        meet_name TEXT NOT NULL,
        meet_date DATE NOT NULL,

        UNIQUE (meet_name, meet_date)
    )
""")

cursor.execute("""
    CREATE TABLE teams (
        team_id INTEGER PRIMARY KEY,
        team_name TEXT NOT NULL UNIQUE,
        team_code TEXT
    )
""")

cursor.execute("""
    CREATE TABLE swimmers (
        swimmer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        team_id INTEGER,

        FOREIGN KEY (team_id) REFERENCES teams(team_id),

        UNIQUE (first_name, last_name, team_id)
    )
""")

cursor.execute("""
    CREATE TABLE events (
        event_id INTEGER PRIMARY KEY,
        meet_id INTEGER NOT NULL,
        event_code TEXT NOT NULL,
        gender TEXT NOT NULL,
        min_age INTEGER,
        max_age INTEGER,
        distance INTEGER NOT NULL,
        course TEXT NOT NULL,
        stroke TEXT NOT NULL,

        FOREIGN KEY (meet_id) REFERENCES meets(meet_id),

        UNIQUE(meet_id, event_code)
    )
""")

#Results
cursor.execute("""
    CREATE TABLE results (
        result_id INTEGER PRIMARY KEY,
        event_id INTEGER NOT NULL,
        meet_id INTEGER NOT NULL,
        swimmer_id INTEGER,
        team_id INTEGER,
        place INTEGER,
        age INTEGER,
        time_seconds REAL,
        display_time TEXT NOT NULL,
        points INTEGER,
        relay_letter TEXT,

        FOREIGN KEY (event_id) REFERENCES events(event_id),
        FOREIGN KEY (meet_id) REFERENCES meets(meet_id),
        FOREIGN KEY (swimmer_id) REFERENCES swimmers(swimmer_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id)

        UNIQUE (event_id, swimmer_id)
    )
""")

cursor.execute("""
    CREATE UNIQUE INDEX unique_relay_result
    ON results(event_id, team_id, relay_letter)
    WHERE relay_letter IS NOT NULL
""")


connection.commit()
connection.close()