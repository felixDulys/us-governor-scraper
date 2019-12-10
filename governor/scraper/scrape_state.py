from governor.config import STATES
from governor.scraper.clean_state import clean_state
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


BASE_URL = "http://en.wikipedia.org/wiki/List_of_governors_of_{capitalized_state}"


def scrape_all_states(out_path):
    print("Initializing all state scrape.")
    all_states = pd.DataFrame()
    # for state in STATES.keys():
    for state in ["Florida", "Alabama"]:
        cleaned_state_df = scrape_state(state)
        all_states = all_states.append(cleaned_state_df)
        all_states.to_csv(f"{out_path}all_states_governors.csv", index=False)


def scrape_state(state_to_scrape):
    print(f"scraping {state_to_scrape}...")
    scraped_state_df = get_state_df_from_wikipedia(state_to_scrape)
    cleaned_state_df = clean_state(scraped_state_df, state_to_scrape)
    return cleaned_state_df


def get_state_df_from_wikipedia(state_to_scrape):
    print(f"setting up browser for {state_to_scrape}...")
    soup, browser = set_up_browser(state_to_scrape)
    match = soup.find_all("table", class_="wikitable sortable jquery-tablesorter", style="text-align:center;")
    # if len(match) > 1:
    # scrub out colonialism.
    match = match[len(match) - 1]

    table_body = match.find('tbody')
    rows = table_body.find_all('tr')

    scraped_state_df = pd.DataFrame(
        columns=["order", "name", "term", "party", "election_year", "starting_year", "lt_govnr"]
    )
    print(f"mining governor data for {state_to_scrape}...")
    leftover_lt_govnrs = []
    df_row = 0
    for row, i in zip(rows, range(0, len(rows))):
        print(f"{i}.", end="")
        cols = row.find_all("td")
        if len(cols) > 2:
            if len(leftover_lt_govnrs) >= 1:
                scraped_state_df.iloc[df_row]["lt_govnr"] = scraped_state_df.iloc[
                    df_row]["lt_govnr"].join(leftover_lt_govnrs)
            leftover_lt_govnrs = []
            df_row = len(scraped_state_df)
            try:
                df = pd.DataFrame(
                    {
                        "order": [cols[0].text.strip()],
                        "name": [cols[1]["data-sort-value"]],
                        "term": [cols[3].text.strip()],
                        "party": [cols[4].text.strip()],
                        "election_year": [cols[5].text.strip()],
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
                        "election_year": [cols[4].text.strip()],
                        "starting_year": [cols[2].text.strip().split(",")[1].strip()[:4]]
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
            except KeyError:
                df = pd.DataFrame(
                    {
                        "order": ["Civil War - Vacated Office"],
                        "name": ["Civil War - Vacated Office"],
                        "term": ["Civil War - Vacated Office"],
                        "party": ["Civil War - Vacated Office"],
                        "election_year": ["Civil War - Vacated Office"],
                        "starting_year": ["Civil War - Vacated Office"]
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
                               chrome_options=option)
    browser.get(BASE_URL.format(capitalized_state=state_to_scrape))
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    return soup, browser


