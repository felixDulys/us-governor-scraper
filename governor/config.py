STATES = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

BASE_URL = "http://en.wikipedia.org/wiki/List_of_governors_of_{capitalized_state}"

COL_FLAGS = {
    "war": "[cC]ivil war|[oO]ccupation",
    "term": "Year|[Tt]erm|[lL]imited|[Vv]acant"
            "Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec |January |February |March |April |May |June |"
            "July |August |"
            "September |October |November |December ",
    "term2": "Years|Term of office|Term in office|term|limited|vacant|Vacant"
            "Jan |Feb |Mar |Apr[ |il ] |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec |January |February |March |April |May "
             "|June |July |August |September |October |November |December ",
    "name": "\A[A-Z]",
    "party": "[Dd]emocrat|[Rr]epublic|Dem|Rep|[Ww]hig|[Uu]nion|[Ff]ederal|[kK]now|[Ppopulist]|[Nn]one|[Ccountry]|[pP]arty|"
             "[Rr]hode ",
}

# These are wikipedia pages with tables that are different from most and need some help.
NO_STYLE = {
    "Mississippi": 2,
    "Missouri": 5,
    "Montana": 2,
    "Nevada": 1,
    "North Carolina": 1,
    "North Dakota": 1,
    "Nebraska": 2,
    "New Hampshire": 2,
    "South Carolina": 1, # tables 1 - 6 are relevant.
    "South Dakota": 1,
    "Vermont": 2,
    "Virginia": 3
}

INCLUDE_HEADERS = [
    "Montana"
]

# todo make this not shit
# order changed for special snowflakes
COL_FLAGS_SPECIAL = {
    "Nevada": {
        "war": COL_FLAGS["war"],
        "name": COL_FLAGS["name"],
        "term": COL_FLAGS["term"],
        "term2": COL_FLAGS["term2"],
        "party": COL_FLAGS["party"],
    },
}
COL_FLAGS_SPECIAL["Washington"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["New Mexico"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["North Carolina"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["South Carolina"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["North Dakota"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["South Dakota"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["Vermont"] = COL_FLAGS_SPECIAL["Nevada"]
COL_FLAGS_SPECIAL["Virginia"] = COL_FLAGS_SPECIAL["Nevada"]

MATCH = ["name", "party"]

## TODO
## Montana - two boxes for term into one.