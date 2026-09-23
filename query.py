import sqlite3
import os

meet_id = 2

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

cursor.execute("SELECT meet_id, meet_name FROM meets")

print("\nMeets:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
    SELECT DISTINCT meet_id
    FROM results
""")

print("\nMeet IDs stored in results:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
    SELECT
        t.team_name,
        s.first_name,
        s.last_name,
        SUM(r.points) AS swimmer_points,
        (
            SELECT SUM(r2.points)
            FROM results r2
            WHERE r2.team_id = t.team_id
              AND r2.meet_id = r.meet_id
        ) AS team_points
    FROM results r
    JOIN swimmers s ON r.swimmer_id = s.swimmer_id
    JOIN teams t ON r.team_id = t.team_id
    WHERE r.meet_id = ?
    GROUP BY
        t.team_id,
        s.swimmer_id
    ORDER BY
        team_points DESC,
        swimmer_points DESC
""", (meet_id,))

rows = cursor.fetchall()

current_team = None

for team, first_name, last_name, swimmer_points, team_points in rows:

    if team != current_team:
        current_team = team
        print(f"\n{team}: {team_points} points")

    print(f"    {first_name} {last_name}: {swimmer_points} points")
connection.close()