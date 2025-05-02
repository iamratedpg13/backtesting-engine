class MomentumStrategy:
    """
    A simple momentum-based trading strategy using Rate of Change (ROC).
    """

    def __init__(self, window: int = 10):
        """
        Initializes the strategy with a specified momentum window.

        Parameters:
            window (int): Lookback period for the Rate of Change (ROC) calculation.
        """
        self.window = window
        self.last_signal = None

    def prepare(self, df) -> None:
        """
        Precomputes the Rate of Change (ROC) indicator.

        Parameters:
            df (pd.DataFrame): Historical price data with 'Close' column.
        """
        df["ROC"] = df["Close"].pct_change(periods=self.window)
        self.df = df

    def generate_signal(self, index: int, row, df) -> str:
        """
        Generates a trading signal based on positive or negative momentum.

        Parameters:
            index (int): Current index in the DataFrame.
            row: Row data at the current index.
            df (pd.DataFrame): Entire historical dataset.

        Returns:
            str: "BUY", "SELL", or "HOLD"
        """
        if index < self.window:
            return "HOLD"

        if row["ROC"] > 0.02 and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return "BUY"
        elif row["ROC"] < -0.02 and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return "SELL"

        return "HOLD"
