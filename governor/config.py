STATES = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    # 'District of Columbia': 'DC',
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
    # 'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    # 'Palau': 'PW',
    'Pennsylvania': 'PA',
    # 'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    # 'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

BASE_URL = "http://en.wikipedia.org/wiki/List_of_governors_of_{capitalized_state}"

COL_FLAGS = {
    "war": "civil war|Civil War|military|occupation",
    # "order": "No.|No|#|[0-100]",
    "name": "\A[A-Z]",
    # "party": "Party|Democrat|Republican|Federalist|party|Independent|Whig",
    "term": "Years|Term of office|Term in office|term|limited|"
            "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|"
            "September|October|November|December",
    "party": "(\w\D)",
    # "lt_govnr": "(Lt.)(\w\D)|exist|war|Civil|War|vacant|Vacant|Office did not exist"
    "lt_govnr": "\A[A-Z]"
}

SORT_COLS = {
    True: {
        "length": None,
        "order": None,
        "name": "data-sort-value",
        "party": None,
        "term": None,
        "lt_govnr": None
    },
    False: {
        "length": None,
        "order": None,
        "name": None,
        "party": None,
        "term": None,
        "lt_govnr": None
    }
}
