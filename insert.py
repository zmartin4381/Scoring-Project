import sqlite3
from dbParser import *


with open("SwimResults/goodOutput.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

    meet_id = -1
    for line in lines:
        event = parse_event(line)

        #print("RAW LINE:", repr(line))
        meet = parse_meet(line)

        if line.startswith("Meet"):
            print("MEET RESULT:", meet)

        if event is not None:
            connection = sqlite3.connect("swim_results.db")
            cursor = connection.cursor()

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
            

            connection.commit()
            connection.close()

        elif meet is not None:
            connection = sqlite3.connect("swim_results.db")
            cursor = connection.cursor()
            
            cursor.execute(
                """
                INSERT OR IGNORE INTO meets (
                    meet_name,
                    meet_date
                )
                VALUES (?, ?)
                """,
                (
                    meet["meet_name"],
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

            connection.commit()
            connection.close()
            
        else:
            pass