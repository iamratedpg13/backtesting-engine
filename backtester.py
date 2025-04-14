import pandas as pd
from core.data_loader import load_data
from core.portfolio import Portfolio
from utils.plotter import Plotter

class Backtester:
    def __init__(self, strategy, data_path, starting_cash):
        self.data = load_data(data_path)
        self.strategy = strategy
        self.portfolio = Portfolio(starting_cash)
        self.plotter = Plotter()
        self.trades = []

    def run(self):
        for index, row in self.data.iterrows():
            action = self.strategy.generate_signal(index, row, self.data)
            if action in ["BUY", "SELL"]:
                self.portfolio.execute_trade(index, row["Close"], action)
                self.trades.append((index, action, row["Close"]))

    def export_results(self):
        self.portfolio.export("results/portfolio_summary.csv")

    def visualize_results(self):
        self.plotter.plot_equity_curve(self.portfolio.history)
        self.plotter.plot_trade_markers(self.data, self.trades)
