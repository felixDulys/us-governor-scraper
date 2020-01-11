from governor.config import COL_FLAGS, BASE_URL
from governor.scraper.clean_state import clean_state
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np


def scrape_all_states(out_path):
    print("Initializing all state scrape.")
    all_states = pd.DataFrame()
    # for state in STATES.keys():
    for state in ["Florida", "Alabama", "Alaska", "Georgia", "Texas", "California", "Massachusetts"]:
        cleaned_state_df = scrape_state(state)
        all_states = all_states.append(cleaned_state_df)
        all_states.to_csv(f"{out_path}all_states_governors_sample_lr.csv", index=False)


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

    sortable = False
    match = None
    for table in tables:
        if (len(table.attrs) >= 1) & ("style" in table.attrs.keys()):
            if ("wikitable" in table.attrs["class"][0]) & ("text-align:" in table.attrs["style"]):
                match = table
                if "sortable" in match.attrs["class"]:
                    sortable = True
        else:
            continue

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
    leftover_lt_govnrs = []
    lt_gov_len = 0
    for row, i in zip(rows, range(0, len(rows))):
        cols = row.find_all("td")
        print(f"col length: {len(cols)} | row: {i}")
        row_key = identify_row(cols, col_flags)
        if row_key["war"] != "no data":
            continue
        else:
            if len(cols) > 3:
                df = pd.DataFrame(
                        {
                            "order": [len(scraped_state_df)],
                            "term": [cols[row_key["term"]].text.strip()],
                            "party": [cols[row_key["party"]].text.strip()],
                            "starting_year": [cols[row_key["term"]].text.strip().split(",")[1].strip()[:4]],
                        }
                )
                if sortable:
                    df = df.assign(name=cols[row_key["name"]]["data-sort-value"])
                else:
                    df = df.assign(name=cols[row_key["name"]].text.strip())
                if isinstance(row_key["lt_govnr"], int) & ((lt_gov_len == len(cols)) | (lt_gov_len == 0)):
                    try:
                        df = df.assign(lt_govnr=cols[row_key["lt_govnr"]]["data-sort-value"])
                    except KeyError:
                        df = df.assign(lt_govnr=cols[row_key["lt_govnr"]].text.strip())
                    lt_gov_len = len(cols)
                elif (len(scraped_state_df) > 0) & (len(leftover_lt_govnrs) == 0):
                    df = df.assign(lt_govnr=scraped_state_df.iloc[len(scraped_state_df) - 1]["lt_govnr"])
                elif len(leftover_lt_govnrs) > 0:
                    if isinstance(row_key["lt_govnr"], int):
                        try:
                            df = df.assign(
                                lt_govnr=cols[row_key["lt_govnr"]]["data-sort-value"].join(leftover_lt_govnrs))
                        except KeyError:
                            df = df.assign(lt_govnr=cols[row_key["lt_govnr"]].text.strip().join(leftover_lt_govnrs))
                else:
                    df = df.assign(lt_govnr=np.nan)
                leftover_lt_govnrs = []
                scraped_state_df = scraped_state_df.append(df)
            elif len(cols) > 0:
                if re.search("\A[A-Z]", cols[len(cols) - 1].text.strip()):
                    try:
                        add_this = cols[len(cols) - 1]["data-sort-value"]
                    except KeyError:
                        add_this = cols[len(cols) - 1].text.strip()
                    leftover_lt_govnrs += [add_this + "| "]
                elif re.search("\d", cols[len(cols) - 1].text.strip()):
                    continue
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
            elif key["lt_govnr"] == "no data":
                key["lt_govnr"] = idx
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


