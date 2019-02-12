
def sma(x, window):
    return x.rolling(5).mean()
