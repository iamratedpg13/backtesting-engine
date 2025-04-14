import pandas as pd

class Portfolio:
    def __init__(self, starting_cash):
        self.cash = starting_cash
        self.holdings = 0
        self.history = []

    def execute_trade(self, date, price, action):
        if action == "BUY" and self.cash >= price:
            self.holdings += 1
            self.cash -= price
        elif action == "SELL" and self.holdings > 0:
            self.holdings -= 1
            self.cash += price
        self.history.append({"Date": date, "Cash": self.cash, "Holdings": self.holdings, "Price": price})

    def export(self, path):
        df = pd.DataFrame(self.history)
        df.to_csv(path, index=False)
