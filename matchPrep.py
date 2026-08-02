import re

with open("SwimResults/output.txt", "r") as file:
    lines = file.readlines()

output = []
good_output = []

for line in lines:
    line = line.strip()

    #Swim Match
    #Ignores anything after points ie Age - Team Name
    #First or is 1 vs 1. or 1)
    #Second or is for time min vs under min
    if re.match(r"(\d+|\d+.)\s+([a-zA-Z0-9])+,\s+([a-zA-Z0-9])+\s+(\d{,2}.\d{2}|\d+:\d{2}.\d{2})\s+(\d{,2})", line):

        good_output.append(line)

    #Event Match
    #First or is for gender matching
    #Second or is for event name vs relay event name
    elif re.match(r"^([^\s]+)\s+(Women|Men|Mixed)\s+(\d+-\d+|Open|(\d+ & Over))\s+(\d{2,4}\w{,3})\s+([a-zA-Z]+\sRelay|[a-zA-Z]+)$", line):

        good_output.append(line)

    #Relay Match
    #First or is for time min vs under min
    #Second or is "Relay - Team Code" VS "Relay* Team Code"
    elif re.match(r"^(\d+)\s+[^\d]*(\d{,2}\.\d{2}|\d+:\d{2}\.\d{2})\s+(Relay)\s+[A-Z](\s+-\s+\w+|.\s+\w+)$", line):

        good_output.append(line)

    #NS Match individual --doesn't need to be processed
    elif re.match(r"(--)\s+([a-zA-Z0-9])+,\s([a-zA-Z0-9])+\s+(NS)\s+(Age)\s+(\d)+\s-\s+(.*)$", line):
        pass
    #NS Relay Match --doesn't need to be processed 

    #Meet Match
    #EX Meet 4 @ Mill Creek Towne — Jul 12, 2026
    elif re.match(r"(\w)+\s+(\d)+\s+(.)\s+([^-])*\s+(\w{3})\s+(\d{,2}),\s+(\d{4})$", line):
        good_output.insert(0, line)

    #Secondary Blank Line Check
    elif not line.strip():
        pass

    #Processes gibberish before name
    elif (
        #Processes place gibberish Normal Name
        #Removes the point check at the end  
            #for cases where time is 20.19. or space exists
        re.match(r"^(\d+).*?([a-zA-Z0-9]+),\s+([a-zA-Z0-9])+\s+(\d{,2}.\d{2}|\d+:\d{2}.\d{2})", line)
        ):
        pass

    #Currently Not Processes
    else:
        output.append(line)

with open ("SwimResults/badOutput.txt", "w") as file:
    for line in output:
        file.write(line + "\n")

with open ("SwimResults/goodOutput.txt", "w") as file:
    for line in good_output:
        file.write(line + "\n")