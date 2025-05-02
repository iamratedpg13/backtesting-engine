import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """
    Loads historical stock data from a CSV file, standardizes column names,
    filters to include only data from 2014, and resets the index.

    Parameters:
        path (str): File path to the CSV containing historical stock data.

    Returns:
        pd.DataFrame: Cleaned and filtered DataFrame containing only 2014 data.
    """
    # Read CSV and parse the 'date' column as datetime
    df = pd.read_csv(path, parse_dates=["date"])

    # Filter for data from the year 2014
    df = df[df["date"].dt.year == 2014].copy()

    # Standardize column names (e.g., 'close' → 'Close')
    df.columns = [col.strip().capitalize() for col in df.columns]

    # Reset index for clean iteration
    return df.reset_index(drop=True)
