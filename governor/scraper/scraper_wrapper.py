from governor.scraper.scrape_state import scrape_all_states
import datetime

OUT_PATH = "~/dta/political/governors/"
DATE = datetime.datetime.now().strftime("%Y-%m-%d")


def main(out_path=OUT_PATH, date=DATE):
    scrape_all_states(out_path, date)


if __name__ == "__main__":
    main()
