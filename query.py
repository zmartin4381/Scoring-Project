import sqlite3
import os

print("Database:", os.path.abspath("swim_results.db"))

connection = sqlite3.connect("swim_results.db")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM events")
count = cursor.fetchone()[0]

print("Number of events:", count)

cursor.execute("SELECT COUNT(*) FROM meets")
count = cursor.fetchone()[0]

print("Number of meets:", count)

connection.close()