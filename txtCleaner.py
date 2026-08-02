import re

with open("SwimResults/meet4.txt", "r") as file:
    lines = file.readlines()

cleaned = []
cleaned.append("")

for line in lines:
    line = line.strip()
    line = re.sub(r"\s+", " ", line)

    if (
        line.startswith("Age") 
        and re.search(r"(\d{,2}|NS|\d{,2}\.)$", cleaned[-1])
        ):  

        if cleaned:
            cleaned[-1] += " " + line

    elif (
        line.startswith("Relay")
        ):

        if cleaned:
            cleaned[-1] += " " + line

    elif (
        re.match(r".\)", line) 
        or line.startswith("PI") 
        or line.__contains__("SwimTopia") 
        or line.startswith("Page") 
        or line.startswith("Download") 
        or line.startswith("Results")
        or line.startswith("More")
    ):
       #ignore line
       pass

    elif not line.strip():
            pass

    else:
        cleaned.append(line)

with open("SwimResults/output.txt", "w") as file:
    for line in cleaned:
        file.write(line + "\n")