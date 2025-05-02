class SampleStrategy:
    """
    A basic moving average crossover strategy for generating trading signals.
    """

    def __init__(self):
        """
        Initializes the strategy with internal memory of the last signal.
        """
        self.last_signal = None

    def generate_signal(self, index: int, row, data) -> str:
        """
        Generates a trading signal based on short- and long-term moving average crossovers.

        Parameters:
            index (int): Current index in the DataFrame.
            row: Current row of data (not used in logic but passed for API compatibility).
            data (pd.DataFrame): Entire historical dataset with 'Close' prices.

        Returns:
            str: "BUY", "SELL", or "HOLD" signal.
        """
        if index < 20:
            return "HOLD"

        short_ma = data["Close"].iloc[max(0, index - 5):index].mean()
        long_ma = data["Close"].iloc[max(0, index - 20):index].mean()

        if short_ma > long_ma and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return "BUY"
        elif short_ma < long_ma and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return "SELL"

        return "HOLD"
