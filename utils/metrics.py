import pandas as pd
import numpy as np


def calculate_total_return(history: list[dict]) -> float:
    """
    Calculates total return over the backtest period.

    Parameters:
        history (list[dict]): List of daily portfolio snapshots.

    Returns:
        float: Total return as a decimal (e.g., 0.15 for 15%).
    """
    if not history:
        return 0.0

    start = history[0]["Cash"] + history[0]["Holdings"] * history[0]["Price"]
    end = history[-1]["Cash"] + history[-1]["Holdings"] * history[-1]["Price"]

    return (end - start) / start


def calculate_max_drawdown(history: list[dict]) -> float:
    """
    Calculates the maximum drawdown in portfolio equity.

    Parameters:
        history (list[dict]): List of daily portfolio snapshots.

    Returns:
        float: Maximum drawdown as a negative decimal (e.g., -0.23 for -23%).
    """
    if not history:
        return 0.0

    df = pd.DataFrame(history)
    df["Equity"] = df["Cash"] + df["Holdings"] * df["Price"]
    cumulative_max = df["Equity"].cummax()
    drawdowns = (df["Equity"] - cumulative_max) / cumulative_max

    return drawdowns.min()


def calculate_win_rate(trades: list[tuple]) -> float:
    """
    Calculates the percentage of profitable buy-sell pairs.

    Parameters:
        trades (list[tuple]): List of executed trades as (Date, Action, Price).

    Returns:
        float: Win rate as a decimal (e.g., 0.6 for 60%).
    """
    if not trades:
        return 0.0

    wins = 0
    total = 0
    previous_action = None
    previous_price = None

    for date, action, price in trades:
        if action == "BUY":
            previous_action = "BUY"
            previous_price = price
        elif action == "SELL" and previous_action == "BUY":
            if price > previous_price:
                wins += 1
            total += 1
            previous_action = None  # Reset after completed pair

    return wins / total if total > 0 else 0.0


def calculate_sharpe_ratio(history: list[dict], risk_free_rate: float = 0.0) -> float:
    """
    Calculates the Sharpe ratio based on daily returns.

    Parameters:
        history (list[dict]): List of daily portfolio snapshots.
        risk_free_rate (float): Annual risk-free rate (default is 0.0).

    Returns:
        float: Sharpe ratio. Returns 0 if standard deviation is zero.
    """
    if not history:
        return 0.0

    df = pd.DataFrame(history)
    df["Equity"] = df["Cash"] + df["Holdings"] * df["Price"]
    df["Returns"] = df["Equity"].pct_change().fillna(0)

    excess_returns = df["Returns"] - (risk_free_rate / 252)

    std_dev = excess_returns.std()
    if std_dev == 0:
        return 0.0

    sharpe = np.sqrt(252) * excess_returns.mean() / std_dev
    return sharpe
