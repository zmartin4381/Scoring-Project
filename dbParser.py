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

result_pattern = re.compile(
    r"^(\d+)\.?\s+"                         # place
    r"([^,]+),\s+"                          # last name
    r"(.+?)\s+"                             # first name
    r"(\d+:\d{2}\.\d{2}|\d+\.\d{2})\s+"     # time
    r"(?:\d+\s+)?"                          # optional points
    r"Age\s+(\d+)\s*-\s*"                   # age
    r"(.+)$"                                # team
)

relay_pattern = re.compile(
    r"^(\d+)\.?\s+"                         # place
    r"(.+?)\s+"                             # team name
    r"(\d+:\d{2}\.\d{2}|\d+\.\d{2})\s+"     # time
    r"Relay\s+([A-Z])\s*"                   # relay A/B/etc.
    r"[-:]\s*"                              # - or :
    r"(.+)$"                                # team code
)

def parse_relay_result(line):
    match = relay_pattern.match(line.strip())

    if not match:
        return None

    return {
        "place": int(match.group(1)),
        "team": match.group(2).strip(),
        "time": match.group(3),
        "relay": match.group(4),
        "team_code": match.group(5).strip()
    }
    
def parse_result(line):
        match = result_pattern.match(line)

        if not match:
            return None
     
        return {
            "place": int(match.group(1)),
            "last_name": match.group(2).strip(),
            "first_name": match.group(3).strip(),
            "time": match.group(4),
            "age": int(match.group(5)),
            "team": match.group(6).strip()
            }

def parse_event(line):
        match = event_pattern.match(line)

        if not match:
                return None

        age_group = match.group(3)
        event_code = match.group(1)
        gender = match.group(2)

        if re.match(r"(\d+-\d+)", age_group):   #Regular Age Group
            ages = age_group.split("-")
            min_age = int(ages[0])    #need to use split data from ages
            max_age = int(ages[1])

        elif re.match(r"Open", age_group):  #Open Age Group
            min_age = 18
            max_age = None
        elif re.match(r"\d+\s+&\s+Over", age_group):    #Mac Age Group
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
    
    date = datetime.strptime(match.group(2), "%b %d, %Y")

    return {
        "meet_name": match.group(1).strip(),
        "meet_date": date.strftime("%Y-%m-%d")
    }

#line = "Meet 4 @ Mill Creek Towne — Jul 12, 2026"
#parse_meet(line)


def calculate_points(place):
    point_values = {
        1: 20,
        2: 17,
        3: 16,
        4: 15,
        5: 14,
        6: 13,
        7: 12,
        8: 11,
        9: 9,
        10: 7,
        11: 6,
        12: 5,
        13: 4,
        14: 3,
        15: 2,
        16: 1
    }

    return point_values.get(place, 0)

def calculate_points_relay(place):
    point_values = {
        1: 40,
        2: 34,
        3: 32,
        4: 30,
        5: 28,
        6: 26,
        7: 24,
        8: 22,
        9: 18,
        10: 14,
        11: 12,
        12: 10,
        13: 8,
        14: 6,
        15: 4,
        16: 2
    }

    return point_values.get(place, 0)

def get_place_from_points(points):
    point_to_place = {
        20: 1,
        17: 2,
        16: 3,
        15: 4,
        14: 5,
        13: 6,
        12: 7,
        11: 8,
        9: 9,
        7: 10,
        6: 11,
        5: 12,
        4: 13,
        3: 14,
        2: 15,
        1: 16
    }

    return point_to_place.get(points)