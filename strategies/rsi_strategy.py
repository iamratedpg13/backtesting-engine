import pandas as pd


class RSIStrategy:
    """
    A strategy based on the Relative Strength Index (RSI) to detect overbought and oversold conditions.
    """

    def __init__(self, period: int = 14, oversold: int = 30, overbought: int = 70):
        """
        Initializes the RSI strategy with threshold parameters.

        Parameters:
            period (int): Number of periods for RSI calculation.
            oversold (int): RSI level considered as oversold (default is 30).
            overbought (int): RSI level considered as overbought (default is 70).
        """
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self.last_signal = None

    def prepare(self, df: pd.DataFrame) -> None:
        """
        Computes the RSI indicator and appends it to the DataFrame.

        Parameters:
            df (pd.DataFrame): Historical price data with 'Close' column.
        """
        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()

        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        self.df = df

    def generate_signal(self, index: int, row, df: pd.DataFrame) -> str:
        """
        Generates a signal based on RSI thresholds.

        Parameters:
            index (int): Current index in the DataFrame.
            row: Row data at the current index.
            df (pd.DataFrame): Full historical dataset.

        Returns:
            str: "BUY", "SELL", or "HOLD"
        """
        if index < self.period:
            return "HOLD"

        if row["RSI"] < self.oversold and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return "BUY"

        elif row["RSI"] > self.overbought and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return "SELL"

        return "HOLD"
