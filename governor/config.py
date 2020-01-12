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
    "war": "civil war|Civil War|military|occupation",
    "term": "Years|Term of office|Term in office|term|limited|"
            "Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec |January |February |March |April |May |June |"
            "July |August |"
            "September |October |November |December ",
    "term2": "Years|Term of office|Term in office|term|limited|"
            "Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec |January |February |March |April |May |June |"
            "July |August |"
            "September |October |November |December ",
    "name": "\A[A-Z]",
    "party": "(\w\D)",
}

# These are wikipedia pages with tables that are different from most and need some help.
NO_STYLE = {
    "Mississippi": 2,
    "Missouri": 5,
    "Montana": 2,
    "Nevada": 1,
    "Nebraska": 2
}

INCLUDE_HEADERS = [
    "Montana"
]

COL_FLAGS_SPECIAL = {
    "Nevada": {
        "war": "civil war|Civil War|military|occupation",
        "name": "\A[A-Z]",
        "term": "Years|Term of office|Term in office|term|limited|"
                "Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec |January |February |March |April |May |June |"
                "July |August |"
                "September |October |November |December ",
        "party": "(\w\D)",
    },
    "Washington": {
        "war": "civil war|Civil War|military|occupation",
        "name": "\A[A-Z]",
        "term": "Years|Term of office|Term in office|term|limited|"
                "Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec |January |February |March |April |May |June |"
                "July |August |"
                "September |October |November |December ",
        "party": "(\w\D)",
    },
}


## TODO
## Montana - two boxes for term into one.