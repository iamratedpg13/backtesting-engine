class BollingerBandStrategy:
    """
    A Bollinger Bands-based strategy that generates signals based on price deviations
    from a moving average envelope.
    """

    def __init__(self, window: int = 20, num_std: int = 2):
        """
        Initializes the strategy with a rolling window and standard deviation multiplier.

        Parameters:
            window (int): Number of periods for the moving average and standard deviation.
            num_std (int): Number of standard deviations for upper and lower bands.
        """
        self.window = window
        self.num_std = num_std
        self.last_signal = None

    def prepare(self, df) -> None:
        """
        Pre-computes Bollinger Bands and adds them to the DataFrame.

        Parameters:
            df (pd.DataFrame): Historical price data with 'Close' column.
        """
        df["SMA"] = df["Close"].rolling(self.window).mean()
        df["STD"] = df["Close"].rolling(self.window).std()
        df["Upper"] = df["SMA"] + self.num_std * df["STD"]
        df["Lower"] = df["SMA"] - self.num_std * df["STD"]
        self.df = df

    def generate_signal(self, index: int, row, df) -> str:
        """
        Generates a signal based on the Bollinger Bands breakout conditions.

        Parameters:
            index (int): Current index in the DataFrame.
            row: Row of price data at the current index.
            df (pd.DataFrame): The full historical price DataFrame.

        Returns:
            str: "BUY", "SELL", or "HOLD" signal.
        """
        if index < self.window:
            return "HOLD"

        if row["Close"] < row["Lower"] and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return "BUY"
        elif row["Close"] > row["Upper"] and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return "SELL"

        return "HOLD"
