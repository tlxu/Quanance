
def sma(df, window):
    return df.rolling(window=window).mean()
