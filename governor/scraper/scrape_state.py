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


def scrape_all_states():
    for state in STATES.keys():
        scrape_state(state)


def scrape_state(state_to_scrape):
    scraped_state_df = get_state_df_from_wikipedia(state_to_scrape)
    cleaned_state_df = clean_state(scraped_state_df)
    return cleaned_state_df


def get_state_df_from_wikipedia(state_to_scrape):
    soup = set_up_browser(state_to_scrape)
    match = soup.find_all("table", class_="wikitable sortable jquery-tablesorter",
                  style="text-align:center;")
    if len(match) > 1:
        # scrub out colonialism.
        match = match[len(match) - 1]

    table_body = match.find('tbody')
    rows = table_body.find_all('tr')

    scraped_state_df = pd.DataFrame(columns=["order", "none", "none2", "term", "party", "year_start", "lt_gov"])
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        # the name is embedded in the col sort value. so get that.

        cols_name = row.find_all("td data-sort-value")


    return scraped_state_df


def set_up_browser(state_to_scrape):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path="/Library/Application Support/Google/chromedriver",
                               chrome_options=option)
    browser.get(BASE_URL.format(capitalized_state=state_to_scrape))
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    return soup


