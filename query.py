import sqlite3
import os

from pathlib import Path

print("Database:", os.path.abspath("swim_results.db"))

connection = sqlite3.connect("swim_results.db")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM events")
count = cursor.fetchone()[0]

print("Number of events:", count)

cursor.execute("SELECT COUNT(*) FROM meets")
count = cursor.fetchone()[0]

print("Number of meets:", count)

cursor.execute("SELECT COUNT(*) FROM swimmers")
count = cursor.fetchone()[0]

print("Number of swimmers:", count)

cursor.execute("SELECT COUNT(*) FROM teams")
count = cursor.fetchone()[0]

print("Number of teams:", count)

cursor.execute("SELECT COUNT(*) FROM results")
count = cursor.fetchone()[0]

print("Number of results:", count)

output_dir = Path("SeasonResults")
output_dir.mkdir(exist_ok=True)

# Get every unique event type in the database
cursor.execute("""
    SELECT DISTINCT
        gender,
        distance,
        stroke
    FROM events
    ORDER BY
        gender,
        distance,
        stroke
""")

events = cursor.fetchall()


for gender, distance, stroke in events:

    # Example: Men25Freestyle
    event = f"{gender}{distance}{stroke.replace(' ', '')}"

    cursor.execute("""
        SELECT
            first_name,
            last_name,
            age,
            display_time,
            meet_name,
            team_name
        FROM (
            SELECT
                s.first_name,
                s.last_name,
                r.age,
                r.display_time,
                m.meet_name,
                r.time_seconds,
                t.team_name,

                ROW_NUMBER() OVER (
                    PARTITION BY s.swimmer_id
                    ORDER BY r.time_seconds
                ) AS rank

            FROM results r

            JOIN events e ON r.event_id = e.event_id
            JOIN swimmers s ON r.swimmer_id = s.swimmer_id
            JOIN meets m ON r.meet_id = m.meet_id
            JOIN teams t ON r.team_id = t.team_id

            WHERE e.gender = ?
              AND e.distance = ?
              AND e.stroke = ?
        )

        WHERE rank = 1
        ORDER BY time_seconds

    """, (
        gender,
        distance,
        stroke
    ))

    rows = cursor.fetchall()

    # Create a unique text file for this event
    filename = output_dir / f"{event}Results.txt"

    with open(filename, "w", encoding="utf-8") as file:

        file.write(
            f"{'Place':<4} "
            f"{'First Name':<12} "
            f"{'Last Name':<12} "
            f"{'Age':<5} "
            f"{'Time':<8} "
            f"{'Meet':<10} "
            f"{'Team':<10}\n"
        )

        file.write("-" * 74 + "\n")

        for place, row in enumerate(rows, start=1):
            first_name, last_name, age, time, meet_name, team_name = row

            file.write(
                f"{place:<5} "
                f"{first_name:<12} "
                f"{last_name:<12} "
                f"{age:<5} "
                f"{time:<8} "
                f"{meet_name:<10} "
                f"{team_name:<10}\n"
            )

    print(f"Created: {filename}")

for gender, distance, stroke in events:

    # Example: Men25Freestyle
    event = f"{gender}{distance}{stroke.replace(' ', '')}"

    cursor.execute("""
        SELECT
            first_name,
            last_name,
            age,
            age_group,
            display_time,
            meet_name,
            team_name
        FROM (
            SELECT
                s.first_name,
                s.last_name,
                r.age,
                r.display_time,
                m.meet_name,
                r.time_seconds,
                t.team_name,

                CASE
                    WHEN r.age BETWEEN 18 AND 29 THEN '18-29'
                    WHEN r.age BETWEEN 30 AND 39 THEN '30-39'
                    WHEN r.age BETWEEN 40 AND 49 THEN '40-49'
                    WHEN r.age BETWEEN 50 AND 59 THEN '50-59'
                    WHEN r.age BETWEEN 60 AND 69 THEN '60-69'
                    WHEN r.age BETWEEN 70 AND 79 THEN '70-79'
                    WHEN r.age >= 80 THEN '80+'
                END AS age_group,

                ROW_NUMBER() OVER (
                    PARTITION BY
                        s.swimmer_id,
                        CASE
                            WHEN r.age BETWEEN 18 AND 29 THEN '18-29'
                            WHEN r.age BETWEEN 30 AND 39 THEN '30-39'
                            WHEN r.age BETWEEN 40 AND 49 THEN '40-49'
                            WHEN r.age BETWEEN 50 AND 59 THEN '50-59'
                            WHEN r.age BETWEEN 60 AND 69 THEN '60-69'
                            WHEN r.age BETWEEN 70 AND 79 THEN '70-79'
                            WHEN r.age >= 80 THEN '80+'
                        END
                    ORDER BY r.time_seconds
                ) AS rank

            FROM results r

            JOIN events e ON r.event_id = e.event_id
            JOIN swimmers s ON r.swimmer_id = s.swimmer_id
            JOIN meets m ON r.meet_id = m.meet_id
            JOIN teams t ON r.team_id = t.team_id

            WHERE e.gender = ?
            AND e.distance = ?
            AND e.stroke = ?
            AND r.age >= 18
        )

        WHERE rank = 1

        ORDER BY
            CASE age_group
                WHEN '18-29' THEN 1
                WHEN '30-39' THEN 2
                WHEN '40-49' THEN 3
                WHEN '50-59' THEN 4
                WHEN '60-69' THEN 5
                WHEN '70-79' THEN 6
                WHEN '80+' THEN 7
            END,
            time_seconds

    """, (
        gender,
        distance,
        stroke
    ))

    rows = cursor.fetchall()

    # Create a unique text file for this event
    filename = output_dir / f"{event}Results.txt"

    with open(filename, "a", encoding="utf-8") as file:

        current_age_group = None
        place = 0

        for first_name, last_name, age, age_group, time, meet_name, team_name in rows:

            if age_group != current_age_group:
                current_age_group = age_group
                place = 1
                file.write("\n")
                file.write(f"{age_group}\n")
                file.write("-" * 74 + "\n")
                
            file.write(
                f"{place:<5} "
                f"{first_name:<12} "
                f"{last_name:<12} "
                f"{age:<5} "
                f"{time:<8} "
                f"{meet_name:<10} "
                f"{team_name:<10}\n"
            )
        


            place += 1


#Prints Meets in DB
cursor.execute("SELECT meet_id, meet_name, meet_location FROM meets")

print("\nMeets:")
for row in cursor.fetchall():
    print(row)

#Prints Teams in DB
cursor.execute("SELECT team_id, team_name, team_code FROM teams")
print("\nTeams:")
for row in cursor.fetchall():
    print(row)

connection.close()