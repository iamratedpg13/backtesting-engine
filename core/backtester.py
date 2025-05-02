import os
import pandas as pd

from core.data_loader import load_data
from core.portfolio import Portfolio
from utils.plotter import Plotter
from utils import metrics


class Backtester:
    """
    Simulates a trading strategy on historical data and tracks performance.
    """

    def __init__(self, strategy, data_path: str, starting_cash: float):
        """
        Initializes the backtester with data, strategy, and portfolio.

        Parameters:
            strategy: A strategy object with a generate_signal() method.
            data_path (str): Path to CSV file with historical stock data.
            starting_cash (float): Initial portfolio cash balance.
        """
        self.data = load_data(data_path)
        self.strategy = strategy
        self.portfolio = Portfolio(starting_cash)
        self.plotter = Plotter()
        self.trades = []  # Stores tuples of (Date, Action, Price)

    def run(self) -> None:
        """
        Runs the backtest by iterating over historical data and executing strategy signals.
        """
        for index, row in self.data.iterrows():
            date = row["Date"]
            price = row["Close"]

            action = self.strategy.generate_signal(index, row, self.data)

            if action in ("BUY", "SELL"):
                self.portfolio.execute_trade(date, price, action)
                self.trades.append((date, action, price))

            self.portfolio.record_equity(date, price)

    def export_results(self, ticker: str) -> None:
        """
        Saves portfolio performance data and metrics for analysis.

        Parameters:
            ticker (str): Stock ticker symbol used for file organization.
        """
        results_dir = os.path.join("results", ticker)
        os.makedirs(results_dir, exist_ok=True)

        equity_df = pd.DataFrame(self.portfolio.history)
        trades_df = pd.DataFrame(self.trades, columns=["Date", "Action", "Price"])

        equity_df.to_csv(os.path.join(results_dir, "equity_curve.csv"), index=False)
        trades_df.to_csv(os.path.join(results_dir, "trades.csv"), index=False)

        total_return = metrics.calculate_total_return(self.portfolio.history)
        max_drawdown = metrics.calculate_max_drawdown(self.portfolio.history)
        win_rate = metrics.calculate_win_rate(self.trades)
        sharpe_ratio = metrics.calculate_sharpe_ratio(self.portfolio.history)

        with open(os.path.join(results_dir, "metrics.txt"), "w") as f:
            f.write(f"Total Return: {total_return * 100:.2f}%\n")
            f.write(f"Max Drawdown: {max_drawdown * 100:.2f}%\n")
            f.write(f"Win Rate: {win_rate * 100:.2f}%\n")
            f.write(f"Sharpe Ratio: {sharpe_ratio:.2f}\n")

        print(f"\nPerformance Metrics for {ticker}:")
        print(f"Total Return: {total_return * 100:.2f}%")
        print(f"Max Drawdown: {max_drawdown * 100:.2f}%")
        print(f"Win Rate: {win_rate * 100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    def visualize_results(self, ticker: str = None, strategy: str = None) -> None:
        """
        Creates and saves visualizations and exports additional performance data.

        Parameters:
            ticker (str, optional): Ticker symbol for result labeling.
            strategy (str, optional): Strategy name for result labeling.
        """
        base_folder = os.path.join("results", ticker or "unknown", strategy or "default")
        os.makedirs(base_folder, exist_ok=True)

        self.plotter.plot_equity_curve(
            self.portfolio.history,
            trades=self.trades,
            ticker=f"{ticker}_{strategy}",
            save_path=os.path.join(base_folder, "equity_curve.png")
        )

        trades_df = pd.DataFrame(self.trades, columns=["Date", "Action", "Price"])
        equity_df = pd.DataFrame(self.portfolio.history)

        trades_df.to_csv(os.path.join(base_folder, "trades.csv"), index=False)
        equity_df.to_csv(os.path.join(base_folder, "equity_curve.csv"), index=False)

        total_return = metrics.calculate_total_return(self.portfolio.history)
        max_drawdown = metrics.calculate_max_drawdown(self.portfolio.history)
        win_rate = metrics.calculate_win_rate(self.trades)
        sharpe_ratio = metrics.calculate_sharpe_ratio(self.portfolio.history)

        with open(os.path.join(base_folder, "metrics.txt"), "w") as f:
            f.write(f"Total Return: {total_return * 100:.2f}%\n")
            f.write(f"Max Drawdown: {max_drawdown * 100:.2f}%\n")
            f.write(f"Win Rate: {win_rate * 100:.2f}%\n")
            f.write(f"Sharpe Ratio: {sharpe_ratio:.2f}\n")
