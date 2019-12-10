from governor.scraper.scrape_state import scrape_all_states

OUT_PATH = "~/dta/political/governors/"


def main(out_path=OUT_PATH):
    scrape_all_states(out_path)


if __name__ == "__main__":
    main()
