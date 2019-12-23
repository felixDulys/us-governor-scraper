from governor.config import STATES
from governor.scraper.clean_state import clean_state
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


BASE_URL = "http://en.wikipedia.org/wiki/List_of_governors_of_{capitalized_state}"


def scrape_all_states(out_path):
    print("Initializing all state scrape.")
    all_states = pd.DataFrame()
    # for state in STATES.keys():
    for state in ["Florida", "Alabama", "Alaska", "Georgia", "Texas", "California", "Massachusetts"]:
        cleaned_state_df = scrape_state(state)
        all_states = all_states.append(cleaned_state_df)
        all_states.to_csv(f"{out_path}all_states_governors_sample.csv", index=False)


def scrape_state(state_to_scrape):
    print(f"scraping {state_to_scrape}...")
    scraped_state_df = get_state_df_from_wikipedia(state_to_scrape)
    cleaned_state_df = clean_state(scraped_state_df, state_to_scrape)
    return cleaned_state_df


def get_state_df_from_wikipedia(state_to_scrape):
    print(f"setting up browser for {state_to_scrape}...")
    soup, browser = set_up_browser(state_to_scrape)
    # match = soup.find_all("table", class_="wikitable sortable jquery-tablesorter", style="text-align:center;")
    match = soup.find_all("table", style="text-align:center;")

    try:
        match = match[len(match) - 1]
    except IndexError:
        try:
            match = soup.find_all("table", style="text-align: center;")
            match = match[len(match) - 1]
        except IndexError:
            match = soup.find_all("table", style="text-align:center")
            match = match[len(match) - 1]

    table_body = match.find('tbody')
    rows = table_body.find_all('tr')

    scraped_state_df = pd.DataFrame(
        columns=["order", "name", "term", "party", "starting_year", "lt_govnr"]
    )
    print(f"mining governor data for {state_to_scrape}...")
    leftover_lt_govnrs = []
    df_row = 0
    for row, i in zip(rows, range(0, len(rows))):
        print(f"{i}.", end="")
        cols = row.find_all("td")
        if len(cols) > 0:
            if len(cols) == 1:
                # for Mass. lt govnr not working.
                continue
            else:
                if len(cols) > 2:
                    if len(leftover_lt_govnrs) >= 1:
                        leftover_lt_govnrs[len(leftover_lt_govnrs) - 1] = leftover_lt_govnrs[len(leftover_lt_govnrs) - 1][:-3]
                        try:
                            scraped_state_df.iloc[df_row]["lt_govnr"] = str(scraped_state_df.iloc[
                                df_row]["lt_govnr"]).join(leftover_lt_govnrs)
                        except IndexError:
                            scraped_state_df.iloc[df_row - 1]["lt_govnr"] = str(scraped_state_df.iloc[
                                df_row - 1]["lt_govnr"]).join(leftover_lt_govnrs)
                    leftover_lt_govnrs = []
                    df_row = len(scraped_state_df)
                    if (len(cols) == 5) | (len(cols) == 4):
                        if cols[0].text.strip() != '—':
                            try:
                                int(cols[0].text.strip())
                                df = pd.DataFrame(
                                    {
                                        "order": [cols[0].text.strip()],
                                        "name": [cols[0].text.strip()],
                                        "term": [cols[1].text.strip()],
                                        "party": [cols[2].text.strip()],
                                        "starting_year": [cols[1].text.strip().split(",")[1].strip()[:4]],
                                        "lt_govnr": [leftover_lt_govnrs]
                                    }
                                )
                            except IndexError:
                                df = pd.DataFrame(
                                    {
                                        "order": [cols[0].text.strip()],
                                        "name": [cols[1]["data-sort-value"]],
                                        "term": [cols[2].text.strip()],
                                        "party": [cols[3].text.strip()],
                                        "starting_year": [cols[2].text.strip().split(",")[1].strip()[:4]],
                                        "lt_govnr": [leftover_lt_govnrs]
                                    }
                                )
                            except ValueError:
                                df = pd.DataFrame(
                                    {
                                        "order": [""],
                                        "name": [cols[0].text.strip()],
                                        "term": [cols[2].text.strip()],
                                        "party": [cols[1].text.strip()],
                                        "lt_govnr": [leftover_lt_govnrs]
                                    }
                                )
                                try:
                                    df = df.assign(
                                        starting_year=[cols[2].text.strip().split(",")[1].strip()[:4]]

                                    )
                                except:
                                    continue
                        else:
                            continue
                    else:
                        try:
                            df = pd.DataFrame(
                                {
                                    "order": [cols[0].text.strip()],
                                    "name": [cols[1]["data-sort-value"]],
                                    "term": [cols[3].text.strip()],
                                    "party": [cols[4].text.strip()],
                                    "starting_year": [cols[3].text.strip().split(",")[1].strip()[:4]]
                                }
                            )
                            try:
                                df = df.assign(
                                    lt_govnr=cols[7]["data-sort-value"]
                                )
                            except IndexError:
                                df = df.assign(
                                    lt_govnr=" "
                                )
                        except IndexError:
                            df = pd.DataFrame(
                                {
                                    "order": [cols[0].text.strip()],
                                    "name": [cols[1]["data-sort-value"]],
                                    "term": [cols[2].text.strip()],
                                    "party": [cols[3].text.strip()],
                                }
                            )
                            try:
                                df = df.assign(
                                    lt_govnr=cols[6]["data-sort-value"]
                                )
                            except IndexError:
                                df = df.assign(
                                    lt_govnr=" "
                                )
                            try:
                                df = df.assign(
                                    starting_year=[cols[2].text.strip().split(",")[1].strip()[:4]]
                                )
                            except IndexError:
                                df = df.assign(
                                    starting_year=cols[2].text.strip()
                                )
                        except KeyError:
                            if i == len(rows):
                                df = np.nan
                            else:
                                df = pd.DataFrame(
                                    {
                                        "order": ["Vacated Office"],
                                        "name": ["Vacated Office"],
                                        "term": ["Vacated Office"],
                                        "party": ["Vacated Office"],
                                        "starting_year": ["Vacated Office"]
                                    }
                                )
                    scraped_state_df = scraped_state_df.append(df)
                else:
                    try:
                        int(cols[len(cols) - 1].text.strip())
                    except ValueError:
                        leftover_lt_govnrs += [cols[len(cols) - 1].text.strip() + " | "]

    return scraped_state_df


def set_up_browser(state_to_scrape):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path="/Library/Application Support/Google/chromedriver",
                               options=option)
    browser.get(BASE_URL.format(capitalized_state=state_to_scrape))
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    return soup, browser


