import pandas as pd

def load_data(path):
    # Read CSV and parse the 'date' column
    df = pd.read_csv(path, parse_dates=["date"])
    
    # Filter for only the year 2014
    df = df[df["date"].dt.year == 2014].copy()
    
    # Standardize column names to Title Case (e.g., 'close' → 'Close')
    df.columns = [col.strip().capitalize() for col in df.columns]

    # Reset index for safety
    return df.reset_index(drop=True)
