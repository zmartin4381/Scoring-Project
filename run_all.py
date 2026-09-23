import os
import subprocess
import sys

DB_FILE = "swim_results.db"

def run_script(script):
    subprocess.run([sys.executable, script], check= True)

print("What would you like to do?")
print("1. Rebuild database")
print("2. Run insert and query")
print("3. Run textCleaner to query")
print("4. Clean data")

choice = input("> ").strip()

if choice == "1":

    # Delete existing database
    if os.path.exists(DB_FILE):
        print(f"\nDeleting {DB_FILE}...")
        os.remove(DB_FILE)

    run_script("tables.py")
    run_script("insert.py")
    run_script("query.py")

elif choice == "2":

    run_script("insert.py")
    run_script("query.py")

elif choice == "3":
    run_script("textCleaner.py")
    run_script("matchPrep.py")
    run_script("insert.py")
    run_script("query.py")

elif choice == "4":

    folder = "SwimResults"

    if os.path.exists(folder):
        for filename in os.listdir(folder):

            if not filename.lower().endswith("results.pdf"):
                file_path = os.path.join(folder, filename)

                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {filename}")

else:
    print("Invalid option.")