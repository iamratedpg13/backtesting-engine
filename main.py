from core.backtester import Backtester
from strategies.sample_strategy import SampleStrategy

files = {
    "AAPL": "data/AAPL_data.csv",
    "AMZN": "data/AMZN_data.csv",
    "MSFT": "data/MSFT_data.csv"
}

for ticker, path in files.items():
    print(f"\n--- Backtesting {ticker} (2014 data) ---")

    strategy = SampleStrategy()
    backtester = Backtester(strategy, data_path=path, starting_cash=10000)

    backtester.run()

    last_price = backtester.data["Close"].iloc[-1]
    final_value = backtester.portfolio.cash + backtester.portfolio.holdings * last_price

    print(f"Final Value: ${final_value:.2f}")
    print(f"Cash: ${backtester.portfolio.cash:.2f}")
    print(f"Holdings: {backtester.portfolio.holdings} shares")
    print(f"Trades: {backtester.trades}")
