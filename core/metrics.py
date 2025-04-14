def calculate_total_return(history):
    if not history:
        return 0
    start = history[0]["Cash"]
    end = history[-1]["Cash"]
    return (end - start) / start
