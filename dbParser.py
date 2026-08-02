import re
from datetime import datetime


event_pattern = re.compile(
    r"^#"
    r"(\d+[A-Z]?)"                          #Event Code 
    r"\s+"
    r"(Women|Men|Mixed)"                    #Gender 
    r"\s+"
    r"(\d+-\d+|Open|\d+\s+&\s+Over)"        #Age Group
    r"\s+"
    r"(\d+)"                                #Distance
    r"(scy|m|lcm)"                          #Course
    r"\s+"
    r"(.+)$"                                #Stroke
)

meet_pattern = re.compile(
    r"^"
    r"([^\-]+)"                             # Meet name
    r"\s+—\s+"                              # Em dash
    r"([A-Za-z]{3}\s+\d{1,2},\s+\d{4})$"    # Date
)

team_pattern = re.compile()

swimmer_pattern = re.compile(
     r"^"
)
    


def parse_event(line):
        match = event_pattern.match(line)

        if not match:
                return None

        if match:
            print(match.groups())
            age_group = match.group(3)

            event_code = match.group(1)
            gender = match.group(2)
            if re.match(r"(\d+-\d+)", age_group):
                ages = age_group.split("-")
                min_age = int(ages[0])    #need to use split data from ages
                max_age = int(ages[1])
            elif re.match(r"Open", age_group):
                min_age = 18
                max_age = None
            elif re.match(r"\d+\s+&\s+Over", age_group):
                ages = age_group.split()
                min_age = int(ages[0])
                max_age = None
            
            distance = int(match.group(4))
            course = match.group(5)
            stroke = match.group(6)

        return {
            "event_code": event_code,
            "gender": gender,
            "min_age": min_age,
            "max_age": max_age,
            "distance": distance,
            "course": course,
            "stroke": stroke,
        }

#line = "#12E Women 60-69 50m Freestyle"
#parse_event(line)

def parse_meet(line):
    match = meet_pattern.match(line)

    if not match:
        return None
    
    if match:
        print(match.groups())
        date = datetime.strptime(match.group(2), "%b %d, %Y")
        meet_name = match.group(1)
        return {
            "meet_name": meet_name,
            "meet_date": date,
        }

#line = "Meet 4 @ Mill Creek Towne — Jul 12, 2026"
#parse_meet(line)
