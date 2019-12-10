import pandas as pd
import numpy as np


def clean_state(dirty_state_df, state_to_scrape):
    cleaned_state_df = dirty_state_df.replace("Äì", " ")
    cleaned_state_df = cleaned_state_df.assign(state=state_to_scrape)
    # from beginning to end of election dupe the row for year matching.
    return cleaned_state_df
