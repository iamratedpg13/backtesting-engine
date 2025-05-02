import pandas as pd


class FrequentTradingStrategy:
    """
    A fast-reacting strategy using EMA crossovers and volatility filtering
    to generate frequent buy/sell signals.
    """

    def __init__(self):
        """
        Initializes internal state for signal tracking and cached DataFrame.
        """
        self.df = None
        self.last_signal = None

    def prepare(self, df: pd.DataFrame) -> None:
        """
        Precomputes indicators needed for signal generation.

        Parameters:
            df (pd.DataFrame): Historical price data with 'Close', 'High', 'Low'.
        """
        df["fast_ema"] = df["Close"].ewm(span=5, adjust=False).mean()
        df["slow_ema"] = df["Close"].ewm(span=20, adjust=False).mean()

        high_low = df["High"] - df["Low"]
        high_close = (df["High"] - df["Close"].shift()).abs()
        low_close = (df["Low"] - df["Close"].shift()).abs()

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        df["atr"] = true_range.rolling(window=14).mean()
        df["volatility"] = df["atr"] / df["Close"]

        self.df = df

    def generate_signal(self, index: int, row, df: pd.DataFrame) -> str:
        """
        Generates a trading signal based on EMA crossover and volatility.

        Parameters:
            index (int): Current row index in the DataFrame.
            row: Row data at the current index (not used directly here).
            df (pd.DataFrame): Historical price data with precomputed indicators.

        Returns:
            str: "BUY", "SELL", or "HOLD"
        """
        if index == 0:
            return "HOLD"

        prev_fast = df["fast_ema"].iloc[index - 1]
        prev_slow = df["slow_ema"].iloc[index - 1]
        curr_fast = df["fast_ema"].iloc[index]
        curr_slow = df["slow_ema"].iloc[index]
        vol = df["volatility"].iloc[index]

        if prev_fast < prev_slow and curr_fast > curr_slow and vol > 0.005:
            self.last_signal = "BUY"
            return "BUY"

        elif prev_fast > prev_slow and curr_fast < curr_slow:
            self.last_signal = "SELL"
            return "SELL"

        return "HOLD"
