import re
import ast
from difflib import SequenceMatcher
from datetime import datetime

KNOWN_TEAMS = [
    ("The Swim Reapers", "TSR"),
    ("The Wet Bandits", "WTBDT"),
    ("Hard Times Swim", "HTST"),
    ("Pooligans", None),
    ("DMV Free Agents", None),
    ("Currents", None),
    ("Wildwood Wombats", None),
    ("Silver Spring", "SPSF"),
    ("Slowbro SC", "SBSC"),
    ("KSCRW", "KSCRW"),
    ("Glenwood Tigers", "GLNWD"),
    ("Somerset Whales", None),
    ("Cool Down Club", "CDC"),
    ("Daleview Pace", None),
    ("WoodPac", "WP"),
    ("WashedWealth", "WW"),
    ("Jimmy's Swim Club", None),
    ("The Heat Strokes", None),
    ("SuitUp Now", None),
    ("STJ Masters", None),
]

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
    r"(Meet\s+\d+)\s+@\s+"                  # Meet name
    r"([a-zA-Z|\s]+)[^\d]+"                 # Meet location
    r"(\w{3})\s+(\d+),\s+(\d{4})"           # Date
)

result_pattern = re.compile(
    r"^(\d+)\.?\s+"                         # place
    r"([^,]+),\s+"                          # last name
    r"(.+?)\s+"                             # first name
    r"(\d+:\d{2}\.\d{2}|\d+\.\d{2})\s+"     # time
    r"Age\s+(\d+)\s*-\s*"                   # age
    r"([\w\s]+)-"                          # team
    r"(\w+)"                                #team code
)

relay_pattern = re.compile(
    r"^(\d+)\.?\s+"                         # place
    r"(.+?)\s+"                             # team name
    r"(\d+:\d{2}\.\d{2}|\d+\.\d{2})\s+"     # time
    r"Relay\s+([A-Z])\s*"                   # relay A/B/etc.
    r"[-:]\s*"                              # - or :
    r"([^-])$"                              # team code
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
            "team": match.group(6).strip(),
            "team_code": match.group(7).strip()
            }

def parse_event(line):
        match = event_pattern.match(line)

        if not match:
                return None

        age_group = match.group(3)
        event_code = match.group(1)
        gender = match.group(2)

        if re.match(r"(\d+-\d+)", age_group):           #Regular Age Group
            ages = age_group.split("-")
            min_age = int(ages[0])    
            max_age = int(ages[1])

        elif re.match(r"Open", age_group):              #Open Age Group
            min_age = 18
            max_age = None
        elif re.match(r"\d+\s+&\s+Over", age_group):    #Max Age Group
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

def parse_meet(line):
    match = meet_pattern.match(line)

    if not match:
        return None
    
    date = datetime.strptime(
        f"{match.group(3)} {match.group(4)}, {match.group(5)}",
        "%b %d, %Y"
    )

    return {
        "meet_name": match.group(1).strip(),
        "meet_location": match.group(2).strip(),
        "meet_date": date.strftime("%Y-%m-%d")
    }


def normalize_team_name(name):
    name = name.lower()

    name = re.sub(r"[^a-z0-9\s]", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()

def match_team(team_name, threshold = 0.8):
    cleaned = normalize_team_name(team_name)

    best_team = None
    best_score = 0
    for name, abbreviation in KNOWN_TEAMS:
        known_cleaned = normalize_team_name(name)

        score = SequenceMatcher(
            None,
            cleaned,
            known_cleaned
        ).ratio()

        if score > best_score:
            best_score = score
            best_team = (name, abbreviation)

        if best_score >= threshold:
            return best_team
    return None


def time_converter(time):
    try:
        num = ast.literal_eval(time)
        if isinstance(num, float):
            return num;
    except:
        return 999.99;

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