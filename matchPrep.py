import re
from dbParser import *

with open("SwimResults/output.txt", "r") as file:
    lines = file.readlines()

output = []
good_output = []

for line in lines:
    line = line.strip()

    #Swim Match
    if re.match(
        r"^[^\d]*(\d+)\.?\s+.*?"                    #place
        r"([a-zA-Z0-9]+)\,\s+"                      #last name
        r"([a-zA-Z0-9]+)\s+"                        #first name
        r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2})",       #time
        line):
        
        swim_match = re.match(
            r"^[^\d]*(\d+)\.?\s+.*?"                #place
            r"([a-zA-Z0-9]+)\,\s+"                  #last name
            r"([a-zA-Z0-9]+)\s+"                    #first name
            r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2})",   #time
        line)

        age_match = re.search(
            r"Age\s+(\d+)"                          #age
            r"[^\w]+(.*)",                          #team
            line
        )

        if swim_match and age_match:
            cleaned_line = (
                f"{swim_match.group(1)} "           #Place
                f"{swim_match.group(2)}, "          #Last Name
                f"{swim_match.group(3)} "           #First Name
                f"{swim_match.group(4)} "           #Time
                f"Age {age_match.group(1)} - "      #Age
                f"{age_match.group(2)}"             #Team
            )

            good_output.append(cleaned_line)

    #Event Match
    elif re.match(
        r"^([^\s]+)\s+"                             #event (#1A)
        r"(Women|Men|Mixed)\s+"                     #gender
        r"(\d+-\d+|Open|(\d+ & Over))\s+"           #age group
        r"(\d{2,4}\w{,3})\s+"                       #distance
        r"([a-zA-Z]+\sRelay|[a-zA-Z]+)$",           #stroke
        line):

        good_output.append(line)

    #Relay Match
    elif re.match(
        r"(\d+|\d+.)\s+[^\d]*"                      #place (ignores team name)
        r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2}).*"      #time
        r"(Relay)",                                 #relay
        line):

        good_output.append(line)

    #NS Match individual --doesn't need to be processed
    elif re.match(
        r"(--)\s+"                                  #place
        r"([a-zA-Z0-9])+,\s"                        #last name
        r"([a-zA-Z0-9])+\s+"                        #first name
        r"(NS)\s+(Age)\s+"                          #NS & Age
        r"(\d)+\s-\s+(.*)$",                        #age num & team
        line):
        pass
    #NS Relay Match --doesn't need to be processed 

    #Meet Match
    #EX Meet 4 @ Mill Creek Towne — Jul 12, 2026
    elif re.match(
        r"(\w)+\s+(\d)+\s+(.)\s+"                   #meet name & num
        r"([^-])*\s+"                               #meet location
        r"(\w{3})\s+(\d{,2}),\s+(\d{4})$",          #meet date
        line):
        good_output.insert(0, line)

    #Secondary Blank Line Check
    elif not line.strip():
        pass

    #Fixes bad time inputs for individuals
    elif re.match(
        r"^(\d+)\s+.*?"                             #place
        r"([a-zA-Z0-9]+),\s+"                       #last name
        r"([a-zA-Z0-9]+)\s+"                        #first name
        r"(\d+)"                                    #time
        , line):
        
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

    #fixes not having a place
    ###NOT DONE WORK ON THIS 
    ### fixes Lozupone, Jude . 43.39 20 Age 65 - Hard Times Swim
    elif re.match(
         r"^([A-Za-z0-9]+),\s+"                     #last name
         r"([A-Za-z0-9]+)\s+.*? "                   #first name
         r"(\d{1,2}\.\d{2}|\d+:\d{2}\.\d{2})\s+"    #time
         r"(\d+)\s+Age\s+"                          #points
         r"(\d+)\s*[-:–—]\s*"                       #age
         r"(.*)$",                                  #rest of line
        line):

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

with open ("SwimResults/badOutput.txt", "w") as file:
    for line in output:
        file.write(line + "\n")

with open ("SwimResults/goodOutput.txt", "w") as file:
    for line in good_output:
        file.write(line + "\n")