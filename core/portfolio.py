import pandas as pd


class Portfolio:
    """
    Manages portfolio state, including cash, holdings, and equity history.
    """

    def __init__(self, starting_cash: float):
        """
        Initializes the portfolio with starting cash and no holdings.

        Parameters:
            starting_cash (float): Initial capital to begin trading with.
        """
        self.cash = starting_cash
        self.holdings = 0
        self.history = []  # Records equity over time

    def execute_trade(self, date, price: float, action: str) -> None:
        """
        Executes a trade based on action and updates portfolio state.

        Parameters:
            date: The current date of the trade.
            price (float): Price per unit of the asset.
            action (str): 'BUY' or 'SELL' trade instruction.
        """
        trade_size = int(self.cash // price) if action == "BUY" else self.holdings

        if action == "BUY" and self.cash >= price:
            self.holdings += trade_size
            self.cash -= trade_size * price
        elif action == "SELL" and self.holdings > 0:
            self.holdings -= trade_size
            self.cash += trade_size * price

        self.history.append({
            "Date": date,
            "Cash": self.cash,
            "Holdings": self.holdings,
            "Price": price
        })

    def record_equity(self, date, price: float) -> None:
        """
        Records daily portfolio value (cash + asset holdings).

        Parameters:
            date: The current date.
            price (float): Price of the asset to value holdings.
        """
        self.history.append({
            "Date": date,
            "Cash": self.cash,
            "Holdings": self.holdings,
            "Price": price
        })

    def export(self, path: str) -> None:
        """
        Exports the recorded portfolio history to a CSV file.

        Parameters:
            path (str): Destination file path for the CSV.
        """
        df = pd.DataFrame(self.history)
        df.to_csv(path, index=False)
