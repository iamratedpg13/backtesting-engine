from core.backtester import Backtester
from strategies.sample_strategy import SampleStrategy

if __name__ == "__main__":
    strategy = SampleStrategy()
    engine = Backtester(strategy)
    engine.run()
