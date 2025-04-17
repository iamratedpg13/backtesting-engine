import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=["date"])
    df = df.sort_values("date")
    
    # Filter only rows from the year 2014
    df = df[df["date"].dt.year == 2014]

    return df.reset_index(drop=True)
