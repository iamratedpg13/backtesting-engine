# Backtesting Engine

A modular and extensible Python engine for simulating, visualizing, and evaluating trading strategies using historical financial data. Designed for rapid research, testing, and strategy iteration.

## Features

- Simulates trades on historical OHLCV data
- Modular strategy design (plug-and-play)
- Visualizes equity curves, buy/sell signals, and holding periods
- Computes key performance metrics:
  - Total Return
  - Max Drawdown
  - Win Rate
  - Sharpe Ratio
- Outputs results to structured folders with CSVs and plots
- Supports batch testing across multiple tickers and strategies

## Project Structure

backtesting-engine/
  core/                         -> Core engine components
    backtester.py              -> Main backtesting logic
    data_loader.py             -> Loads and filters historical data
    portfolio.py               -> Manages trades, cash, and holdings

  strategies/                  -> Trading strategy definitions
    sample_strategy.py
    bollinger_band_strategy.py
    frequent_trading_strategy.py
    momentum_strategy.py
    rsi_strategy.py

  utils/                       -> Utility modules
    metrics.py                 -> Performance metric calculations
    plotter.py                 -> Equity curve and metrics plot generator

  data/                        -> Input CSV data
    AAPL_data.csv, etc.

  results/                     -> Output directory (auto-generated)
    [ticker]/[strategy]/       -> Equity curve, trades, metrics, plots

  main.py                      -> Main CLI runner
  requirements.txt             -> Dependency list
  README.md                    -> This file

## Installation

Python 3.8+ is required.

Install all dependencies:
  pip install -r requirements.txt

Contents of requirements.txt:
  pandas>=1.3.0
  numpy>=1.21.0
  matplotlib>=3.4.0

## Getting Started

1. Place historical CSV files in the `data/` directory.
   Each file should include:
     - Date, Open, High, Low, Close, Volume

2. Run the backtesting engine:
     python main.py

3. Select:
   - A ticker (e.g., AAPL or ALL)
   - A strategy (e.g., RSIStrategy or ALL)

4. Results will be saved in the `results/` folder with plots, metrics, and summary CSVs.

## Built-In Strategies

SampleStrategy           - Simple moving average crossover
RSIStrategy              - Uses RSI thresholds to generate signals
BollingerBandStrategy    - Trades on breakouts from Bollinger Bands
FrequentTradingStrategy  - EMA crossovers + volatility filter
MomentumStrategy         - Momentum via Rate of Change (ROC)

To add your own strategy:
- Define `generate_signal(self, index, row, data)`
- Optionally add `prepare(self, df)` to precompute indicators

## Output Example

Final output includes:
- equity_curve.png
- equity_curve.csv
- trades.csv
- metrics.txt
- summary.csv (aggregates all runs)

Example metrics:
  Total Return: 15.43%
  Max Drawdown: -10.15%
  Win Rate: 57.1%
  Sharpe Ratio: 1.25

## Future Improvements

- Support for slippage and transaction costs
- Position sizing / risk management
- GUI

## License

MIT License.

