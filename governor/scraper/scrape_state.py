from governor.config import COL_FLAGS, BASE_URL, STATES, NO_STYLE
from governor.scraper.clean_state import clean_state
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re

# todo: go back and hard code parties for accuarcy


def scrape_all_states(out_path):
    print("Initializing all state scrape.")
    all_states = pd.DataFrame()
    for state in STATES.keys():
    # for state in ["Mississippi"]:
        cleaned_state_df = scrape_state(state)
        all_states = all_states.append(cleaned_state_df)
        all_states.to_csv(f"{out_path}all_states_governors_sample_nolt.csv", index=False)


def scrape_state(state_to_scrape):
    print(f"scraping {state_to_scrape}...")
    scraped_state_df = get_state_df_from_wikipedia(state_to_scrape)
    cleaned_state_df = clean_state(scraped_state_df, state_to_scrape)
    return cleaned_state_df


def get_state_df_from_wikipedia(state_to_scrape, col_flags=COL_FLAGS):
    print(f"setting up browser for {state_to_scrape}...")
    soup, browser = set_up_browser(state_to_scrape)

    # grab all tables from the page
    tables = soup.find_all("table")

    match = None
    i = 0
    for table in tables:
        if state_to_scrape in NO_STYLE:
            if (len(table.attrs) >= 1) & ("wikitable" in table.attrs["class"][0]):
                match = table
                i += 1
                if i == 2:
                    break
        else:
            if (len(table.attrs) >= 1) & ("style" in table.attrs.keys()):
                if ("wikitable" in table.attrs["class"][0]) & ("text-align:" in table.attrs["style"]):
                    match = table
            # else:
            #     continue

    if match is not None:
        table_body = match.find('tbody')
    else:
        raise Exception("No valid table on this page.")

    rows = table_body.find_all('tr')

    headers = list(col_flags.keys())
    headers.remove("war")

    scraped_state_df = pd.DataFrame(
        columns=["starting_year"] + headers
    )
    print(f"mining governor data for {state_to_scrape}...")
    for row, i in zip(rows, range(0, len(rows))):
        cols = row.find_all("td")
        print(f"col length: {len(cols)} | row: {i}")
        row_key = identify_row(cols, col_flags)
        if row_key["war"] != "no data":
            continue
        else:
            if len(cols) > 3:
                if row_key["party"] == "no data":
                    if len(row.find_all("th")) > 0:
                        cols = [row.find_all("th")[0]] + cols
                        row_key = identify_row(cols, col_flags)
                        if row_key["party"] == "no data":
                            party = "None"
                    else:
                        continue
                else:
                    party = cols[row_key["party"]].text.strip()
                if row_key["term"] == "no data":
                    continue
                else:
                    starting_year = cols[row_key["term"]].text.strip().split(",")[1].strip()[:4]

                df = pd.DataFrame(
                        {
                            "order": [len(scraped_state_df)],
                            "term": [cols[row_key["term"]].text.strip()],
                            "party": [party],
                            "starting_year": [starting_year],
                        }
                )
                if "data-sort-value" in cols[row_key["name"]].attrs:
                    df = df.assign(name=cols[row_key["name"]]["data-sort-value"])
                else:
                    df = df.assign(name=cols[row_key["name"]].text.strip())
                scraped_state_df = scraped_state_df.append(df)
            else:
                continue

    return scraped_state_df


def identify_row(cols, col_flags):
    # make sure that we mirror col flags object.
    key = dict()
    for col in col_flags.keys():
        key[col] = "no data"
    # match the columns to their locations by header
    for cell, idx in zip(cols, range(0, len(cols))):
        if "data-sort-value" in cell.attrs.keys():
            if key["name"] == "no data":
                key["name"] = idx
        else:
            this_col = cell.text.strip()
            for col in key.keys():
                if key[col] == "no data":
                    if re.search(col_flags[col], this_col):
                        key[col] = idx
                        break
        if key["war"] != "no data":
            break
    return key


def set_up_browser(state_to_scrape):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path="/Library/Application Support/Google/chromedriver",
                               options=option)
    browser.get(BASE_URL.format(capitalized_state=state_to_scrape))
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    return soup, browser


