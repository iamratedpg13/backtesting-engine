class SampleStrategy:
    def __init__(self):
        self.last_signal = None

    def generate_signal(self, index, row, data):
        if index < 20:
            return "HOLD"
        short_ma = data["Close"].iloc[max(0, index-5):index].mean()
        long_ma = data["Close"].iloc[max(0, index-20):index].mean()
        if short_ma > long_ma and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return "BUY"
        elif short_ma < long_ma and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return "SELL"
        return "HOLD"
