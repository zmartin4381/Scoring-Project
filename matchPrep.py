import re
from dbParser import *

with open("TextProcessing/cleaned.txt", "r") as file:
    lines = file.readlines()

output = []
good_output = []

for line in lines:
    line = line.strip()


    swim_match = re.match(
    r"^[^\d]*(\d+).?\s+.*?"                 #place
    r"([a-zA-Z0-9]+)\,\s+"                  #last name
    r"([a-zA-Z0-9]+)[^\d]+"                 #first name
    r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2})",   #time
    line)

    event_match = re.match(
        r"^([^\s]+)\s+"                             #event (#1A)
        r"(Women|Men|Mixed)\s+"                     #gender
        r"(\d+-\d+|Open|(\d+ & Over))\s+"           #age group
        r"(\d{2,4}\w{,3})\s+"                       #distance
        r"([a-zA-Z]+\sRelay|[a-zA-Z]+)$",           #stroke
        line)

    relay_match = re.match(
        r"(\d+|\d+.)\s+[^\d]*"                      #place (ignores team name)
        r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2}).*"      #time
        r"(Relay)",                                 #relay
        line)

    NS_match = re.match(
        r"(--)\s+"                                  #place
        r"([a-zA-Z0-9])+,\s"                        #last name
        r"([a-zA-Z0-9])+\s+"                        #first name
        r"(NS)\s+(Age)\s+"                          #NS & Age
        r"(\d)+\s-\s+(.*)$",                        #age num & team
        line)

    meet_match = re.match(
        r"Meet\s+(\d+)\s+@\s+"                      #meet num
        r"([a-zA-Z\s]+?)\s+-\s+"                     #meet location
        r"(\w{3})\s+(\d+),\s+(\d{4})",                         #meet date
        line)

    wonky_time = re.match(
        r"^(\d+)\s+.*?"                             #place
        r"([a-zA-Z0-9]+),\s+"                       #last name
        r"([a-zA-Z0-9]+)\s+"                        #first name
        r"(\d+)"                                    #time
        , line)

    wonky_place = re.match(
         r"^([A-Za-z0-9]+),\s+"                     #last name
         r"([A-Za-z0-9]+)\s+.*? "                   #first name
         r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2})\s+"    #time
         r"(\d+)\s+Age\s+"                          #points
         r"(\d+)\s*[-:–—]\s*"                       #age
         r"(.*)$",                                  #rest of line
        line)

    #Swim Match
    if swim_match:
        age_match = re.search(
            r"Age\s+(\d+)"                          #age
            r"[^\w]+(.*)$",                         #team
            line
        )

        if swim_match and age_match:
            team = match_team(age_match.group(2))

            if team:
                team_name, team_code = team
                team = f"{team_name}-{team_code}"

            cleaned_line = (
                f"{swim_match.group(1)} "           #Place
                f"{swim_match.group(2)}, "          #Last Name
                f"{swim_match.group(3)} "           #First Name
                f"{swim_match.group(4)} "           #Time
                f"Age {age_match.group(1)} - "      #Age
                f"{team}"                           #Team
            )

            good_output.append(cleaned_line)

    #Event Match
    elif event_match:
        good_output.append(line)

    #Relay Match
    elif relay_match:

        good_output.append(line)

    #NS Match individual --doesn't need to be processed
    elif NS_match:
        pass

    #Meet Match
    #EX Meet 4 @ Mill Creek Towne — Jul 12, 2026
    elif meet_match:
        meet_num = meet_match.group(1)
        location = meet_match.group(2).strip()
        month = meet_match.group(3)
        day = meet_match.group(4)

        cleaned_line = f"Meet {meet_num} @ {location} - {month} {day}, 2026"

        good_output.append(cleaned_line)

    #Secondary Blank Line Check
    elif not line.strip():
        pass

    #Fixes bad time inputs for individuals
    elif wonky_time:
        
        match = re.match(
            r"^(\d+)\s+.*?"                         #place
            r"([a-zA-Z0-9]+),\s+"                   #last name
            r"([a-zA-Z0-9]+)\s+"                    #first name
            r"(\d+)"                                #time
            r"(.*)$",                               #rest of line
            line
        )

        time = match.group(4)
        time = time[:-2] +"." + time[-2:]

        cleaned_line = (
            f"{match.group(1)} "    #Place
            f"{match.group(2)}, "   #Last Name
            f"{match.group(3)} "    #First Name
            f"{time}"               #Time
            f"{match.group(5)}"
        )
        good_output.append(cleaned_line)

    #fixes not having a place
    ### fixes Lozupone, Jude . 43.39 20 Age 65 - Hard Times Swim
    elif wonky_place:

        missing_place_match = re.match(
         r"^([A-Za-z0-9]+),\s+"                     #last name
         r"([A-Za-z0-9]+)\s+.*? "                   #first name
         r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2})\s+"    #time
         r"(\d+)\s+Age\s+"                          #points
         r"(\d+)\s*[-:–—]\s*"                       #age
         r"(.*)$",                                  #rest of line
        line)
        
        points = int(missing_place_match.group(4))
        place = get_place_from_points(points)

        if place is not None:
                cleaned_line = (
                    f"{place} "
                    f"{missing_place_match.group(1)}, "
                    f"{missing_place_match.group(2)} "
                    f"{missing_place_match.group(3)} "
                    f"Age {missing_place_match.group(5)} - "
                    f"{missing_place_match.group(6)}"
                )

                good_output.append(cleaned_line)

    #Currently Not Processes
    else:
        output.append(line)

with open ("TextProcessing/badOutput.txt", "a") as file:
    for line in output:
        file.write(line + "\n")

with open ("TextProcessing/goodOutput.txt", "a") as file:
    for line in good_output:
        file.write(line + "\n")