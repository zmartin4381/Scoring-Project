import sqlite3
from dbParser import *

connection = sqlite3.connect("swim_results.db")
cursor = connection.cursor()

with open("TextProcessing/goodOutput.txt", "r", encoding="utf-8") as file, \
     open("TextProcessing/unparsed.txt", "w", encoding="utf-8") as unparsed_file:
    lines = file.readlines()

    meet_id = -1
    event_id = -1

    for line in lines:
        # parse/insert everything here
        meet = parse_meet(line)
        event = parse_event(line)
        result = parse_result(line)
        relay = parse_relay_result(line)

        if meet is not None:
            cursor.execute(
                """
                INSERT OR IGNORE INTO meets (
                    meet_name,
                    meet_location,
                    meet_date
                )
                VALUES (?, ?, ?)
                """,
                (
                    meet["meet_name"],
                    meet["meet_location"],
                    meet["meet_date"],
                ),
            )

            cursor.execute(
                """
                SELECT meet_id
                FROM meets
                WHERE meet_name = ? AND meet_date = ?
                """,
                (
                    meet["meet_name"],
                    meet["meet_date"],
                ),
            )

            meet_id = cursor.fetchone()[0]

        elif event is not None:
            cursor.execute(
                """
                INSERT OR IGNORE INTO events (
                    meet_id,
                    event_code,
                    gender,
                    min_age,
                    max_age,
                    distance,
                    course,
                    stroke
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    meet_id,
                    event["event_code"],
                    event["gender"],
                    event["min_age"],
                    event["max_age"],
                    event["distance"],
                    event["course"],
                    event["stroke"],
                ),
            )

            cursor.execute(
                """
                SELECT event_id
                FROM events
                WHERE meet_id = ? AND event_code = ?
                """,
                (
                    meet_id,
                    event["event_code"]
                )
            )

            event_id = cursor.fetchone()[0]

        elif result is not None:
            cursor.execute(
                """
                INSERT OR IGNORE INTO teams (
                team_name,
                team_code
                )
                VALUES (?, ?)
                """,
                (
                    result["team"],
                    result["team_code"]
                )
            )

            cursor.execute(
                """
                SELECT team_id
                FROM teams
                WHERE team_name = ?
                """,
                (result["team"],)
            )

            team_id = cursor.fetchone()[0]

            cursor.execute(
                    """
                    INSERT OR IGNORE INTO swimmers (
                        first_name,
                        last_name,
                        team_id
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        result["first_name"],
                        result["last_name"],
                        team_id
                    )
                )

            cursor.execute(
                """
                SELECT swimmer_id
                FROM swimmers
                WHERE first_name = ?
                AND last_name = ?
                AND team_id = ?
                """,
                (
                    result["first_name"],
                    result["last_name"],
                    team_id
                )
            )

            swimmer_id = cursor.fetchone()[0]
            points = calculate_points(result["place"])
            time_seconds = time_converter(result["time"])

            cursor.execute(
                """
                INSERT OR IGNORE INTO results (
                    event_id,
                    meet_id,
                    swimmer_id,
                    team_id,
                    place,
                    age,
                    display_time,
                    time_seconds,
                    points
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    meet_id,
                    swimmer_id,
                    team_id,
                    result["place"],
                    result["age"],
                    result["time"],
                    time_seconds,
                    points
                )
            )

        elif relay is not None:
            cursor.execute("""
                INSERT OR IGNORE INTO teams (
                    team_name,
                    team_code
                )
                VALUES (?, ?)
            """, (
                relay["team"],
                relay["team_code"]
            ))

            cursor.execute("""
                SELECT team_id
                FROM teams
                WHERE team_name = ?
            """, (
                relay["team"],
            ))

            team_id = cursor.fetchone()[0]
            points = calculate_points_relay(relay["place"])

            cursor.execute("""
                    INSERT OR IGNORE INTO results (
                        event_id,
                        meet_id,
                        swimmer_id,
                        team_id,
                        place,
                        age,
                        display_time,
                        points,
                        relay_letter
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event_id,
                    meet_id,
                    None,                   # no individual swimmer
                    team_id,
                    relay["place"],
                    None,                   # no individual age
                    relay["time"],
                    points,
                    relay["relay"]
                ))

        else:
            unparsed_file.write(line)

connection.commit()
connection.close()