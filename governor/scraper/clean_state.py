import pandas as pd
import numpy as np


def clean_state(dirty_state_df, state_to_scrape):
    cleaned_state_df = dirty_state_df.replace(
        "Äì", " ").replace("î", "").replace("[i]", "").replace("[q]", "").replace("Ä", "").replace(
        "[al]", "").replace("—", "")
    cleaned_state_df = cleaned_state_df.assign(
        state=state_to_scrape,
        exit_year=cleaned_state_df.starting_year.shift(-1)
    )
    cleaned_state_df = cleaned_state_df.loc[cleaned_state_df.name != "Vacated Office"]
    # from beginning to end of election dupe the row for year matching.
    return cleaned_state_df
