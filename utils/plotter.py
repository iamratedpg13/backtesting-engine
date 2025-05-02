import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as mticker
import matplotlib

from utils import metrics

matplotlib.rcParams['toolbar'] = 'None'


class Plotter:
    """
    Generates equity curve visualizations and displays key performance metrics.
    """

    def plot_equity_curve(
        self,
        history: list[dict],
        trades: list[tuple] = None,
        ticker: str = None,
        save_path: str = None
    ) -> None:
        """
        Plots the equity curve and performance metrics from a backtest.

        Parameters:
            history (list[dict]): Daily portfolio snapshots (cash, holdings, price).
            trades (list[tuple], optional): List of (Date, Action, Price) tuples.
            ticker (str, optional): Ticker symbol for labeling the chart.
            save_path (str, optional): Path to save the plot as an image. If None, shows interactively.
        """
        df = pd.DataFrame(history)
        df["Equity"] = df["Cash"] + df["Holdings"] * df["Price"]

        # --- Calculate Metrics ---
        total_return = metrics.calculate_total_return(history)
        max_drawdown = metrics.calculate_max_drawdown(history)
        sharpe_ratio = metrics.calculate_sharpe_ratio(history)
        win_rate = metrics.calculate_win_rate(trades) if trades else 0.0

        # --- Create Figure with Subplots ---
        fig, (ax_curve, ax_metrics) = plt.subplots(
            1, 2, figsize=(14, 5),
            gridspec_kw={'width_ratios': [4, 1]}
        )

        # --- Plot Equity Curve ---
        ax_curve.plot(df["Date"], df["Equity"], label="Equity Curve", linewidth=2)
        ax_curve.set_title(
            f"Equity Curve with Trades - {ticker}" if ticker else "Equity Curve with Trades"
        )
        ax_curve.set_xlabel("Date")
        ax_curve.set_ylabel("Portfolio Value ($)")
        ax_curve.grid(True)
        ax_curve.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))

        # --- Plot Buy/Sell Trade Markers ---
        if trades:
            buy_labeled = False
            sell_labeled = False
            for trade_date, action, _ in trades:
                match = df[df["Date"] == trade_date]
                if not match.empty:
                    equity_value = match["Equity"].values[0]
                    color = "g" if action == "BUY" else "r"
                    label = None
                    if action == "BUY" and not buy_labeled:
                        label = "BUY"
                        buy_labeled = True
                    elif action == "SELL" and not sell_labeled:
                        label = "SELL"
                        sell_labeled = True
                    ax_curve.scatter(
                        trade_date, equity_value,
                        color=color, label=label, s=60, edgecolors='black'
                    )
            ax_curve.legend()

        # --- Highlight In-Position Ranges ---
        if trades:
            in_position = False
            start_date = None
            for trade_date, action, _ in trades:
                if action == "BUY" and not in_position:
                    start_date = trade_date
                    in_position = True
                elif action == "SELL" and in_position:
                    end_date = trade_date
                    ax_curve.axvspan(start_date, end_date, color='green', alpha=0.1)
                    in_position = False
            if in_position:
                last_date = df["Date"].iloc[-1]
                ax_curve.axvspan(start_date, last_date, color='green', alpha=0.1)

        # --- Display Performance Metrics ---
        ax_metrics.axis('off')
        metrics_data = [
            ("Total Return", f"{total_return * 100:.2f}%", "green" if total_return >= 0 else "red"),
            ("Max Drawdown", f"{max_drawdown * 100:.2f}%", "red" if max_drawdown < 0 else "green"),
            ("Win Rate", f"{win_rate * 100:.2f}%", "green" if win_rate >= 0.5 else "red"),
            ("Sharpe Ratio", f"{sharpe_ratio:.2f}", "green" if sharpe_ratio >= 1 else "red")
        ]

        spacing = 0.15
        y_start = 1.0
        for i, (label, value, color) in enumerate(metrics_data):
            y_pos = y_start - i * spacing
            rect = patches.FancyBboxPatch(
                (0, y_pos - 0.1), 1, 0.1,
                boxstyle="round,pad=0.02",
                facecolor=color,
                edgecolor='black',
                linewidth=1,
                alpha=0.3
            )
            ax_metrics.add_patch(rect)
            ax_metrics.text(
                0.5, y_pos - 0.05,
                f"{label}: {value}",
                fontsize=10,
                ha="center",
                va="center",
                weight='bold'
            )

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
