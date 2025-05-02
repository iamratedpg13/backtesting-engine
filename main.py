import os
import pandas as pd

from core.backtester import Backtester
from strategies.sample_strategy import SampleStrategy
from strategies.frequent_trading_strategy import FrequentTradingStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.bollinger_band_strategy import BollingerBandStrategy
from strategies.momentum_strategy import MomentumStrategy
from utils import metrics


# Available tickers and their data file paths
files = {
    "AAPL": "data/AAPL_data.csv",
    "AMZN": "data/AMZN_data.csv",
    "BA":   "data/BA_data.csv",
    "F":    "data/F_data.csv",
    "GE":   "data/GE_data.csv",
    "HD":   "data/HD_data.csv",
    "JNJ":  "data/JNJ_data.csv",
    "MCD":  "data/MCD_data.csv",
    "MSFT": "data/MSFT_data.csv",
    "NVDA": "data/NVDA_data.csv"
}

# Available strategy classes
available_strategies = {
    "SampleStrategy": SampleStrategy,
    "FrequentTradingStrategy": FrequentTradingStrategy,
    "RSIStrategy": RSIStrategy,
    "BollingerBandStrategy": BollingerBandStrategy,
    "MomentumStrategy": MomentumStrategy
}

# Prompt user to select ticker and strategy
print("Available Tickers:")
for ticker in files:
    print(f"- {ticker}")
print("- ALL")

selected_ticker = input("\nEnter the ticker you want to backtest (or 'ALL'): ").strip().upper()

print("\nAvailable Strategies:")
for name in available_strategies:
    print(f"- {name}")
print("- ALL")

selected_strategy_name = input("\nEnter the strategy you want to use (or 'ALL'): ").strip()

# Determine tickers and strategies to run
tickers_to_run = list(files.keys()) if selected_ticker == "ALL" else [selected_ticker]
strategies_to_run = (
    list(available_strategies.items())
    if selected_strategy_name == "ALL"
    else [(selected_strategy_name, available_strategies.get(selected_strategy_name))]
)

# Store results for summary
summary_data = []

for ticker in tickers_to_run:
    if ticker not in files:
        print(f"Ticker '{ticker}' not found. Skipping.")
        continue

    for strategy_name, StrategyClass in strategies_to_run:
        if StrategyClass is None:
            print(f"Strategy '{strategy_name}' not found. Skipping.")
            continue

        print(f"\n--- Backtesting {ticker} with {strategy_name} ---")

        strategy = StrategyClass()
        backtester = Backtester(strategy, data_path=files[ticker], starting_cash=10000)

        if hasattr(strategy, "prepare"):
            strategy.prepare(backtester.data)

        backtester.run()

        # Compute final portfolio value
        last_price = backtester.data["Close"].iloc[-1]
        final_value = backtester.portfolio.cash + backtester.portfolio.holdings * last_price

        print(f"Final Value: ${final_value:.2f}")
        print(f"Cash: ${backtester.portfolio.cash:.2f}")
        print(f"Holdings: {backtester.portfolio.holdings} shares")
        print(f"Trades: {len(backtester.trades)}")

        # Visualize and export results
        backtester.visualize_results(ticker=ticker, strategy=strategy_name)

        # Compute and store metrics
        ret = metrics.calculate_total_return(backtester.portfolio.history)
        dd = metrics.calculate_max_drawdown(backtester.portfolio.history)
        win_rate = metrics.calculate_win_rate(backtester.trades)
        sharpe = metrics.calculate_sharpe_ratio(backtester.portfolio.history)

        summary_data.append({
            "Ticker": ticker,
            "Strategy": strategy_name,
            "Final Value": round(final_value, 2),
            "Total Return (%)": round(ret * 100, 2),
            "Max Drawdown (%)": round(dd * 100, 2),
            "Win Rate (%)": round(win_rate * 100, 2),
            "Sharpe Ratio": round(sharpe, 2)
        })

# Save summary table
if summary_data:
    summary_df = pd.DataFrame(summary_data)
    os.makedirs("results", exist_ok=True)
    summary_df.to_csv("results/summary.csv", index=False)
    print("\nSummary written to results/summary.csv")
else:
    print("\nNo valid backtests were completed.")
