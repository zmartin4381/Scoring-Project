import os
from pathlib import Path
import subprocess
import sys
import shutil

DB_FILE = "swim_results.db"


def run_script(script, *args):
    print(f"\n--- Running {script} {' '.join(map(str, args))} ---")

    subprocess.run(
        [sys.executable, script, *map(str, args)],
        check=True
    )

print("What would you like to do?")
print("1. Rebuild database")
print("2. Run textCleaner to query")
print("3. Run insert and query")
print("4. Run all")
print("9. Clean data")

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
    run_script("textCleaner.py")
    run_script("matchPrep.py")
    run_script("insert.py")
    run_script("query.py")


elif choice == "3":
    run_script("insert.py")
    run_script("query.py")


elif choice == "4":

    folder = Path("SwimResults")

    for pdf_file in folder.glob("*.pdf"):
        print(f"\nProcessing: {pdf_file.name}")

        run_script("pdfToText.py", pdf_file)
        run_script("textCleaner.py")
        run_script("matchPrep.py")
        #run_script("insert.py")

    #run_script("query.py")


elif choice == "9":

    folder = "SwimResults"

    if os.path.exists(folder):
        for filename in os.listdir(folder):

            if filename.lower().endswith("ocr.pdf"):
                file_path = os.path.join(folder, filename)

                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {filename}")

    folder = "TextProcessing"
    
    if os.path.exists(folder):
        for filename in os.listdir(folder):

            if filename.lower().endswith(".txt"):
                file_path = os.path.join(folder, filename)

                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {filename}")

    shutil.rmtree("__pycache__")

else:
    print("Invalid option.")