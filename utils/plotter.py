import matplotlib.pyplot as plt
import pandas as pd

class Plotter:
    def plot_equity_curve(self, history):
        df = pd.DataFrame(history)
        df["Equity"] = df["Cash"] + df["Holdings"] * df["Price"]
        plt.plot(df["Date"], df["Equity"])
        plt.title("Equity Curve")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.show()

    def plot_trade_markers(self, data, trades):
        plt.plot(data.index, data["Close"], label="Close Price")
        for date, action, price in trades:
            color = "g" if action == "BUY" else "r"
            plt.scatter(date, price, color=color, label=action)
        plt.title("Trades on Price Chart")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.show()
