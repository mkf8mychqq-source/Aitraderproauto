import pandas as pd


def ema(series: pd.Series, length: int):
    return series.ewm(span=length, adjust=False).mean()


def rsi(series: pd.Series, length: int = 14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(length).mean()
    loss = (-delta.clip(upper=0)).rolling(length).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series):
    fast = ema(series, 12)
    slow = ema(series, 26)
    line = fast - slow
    signal = ema(line, 9)
    hist = line - signal
    return line, signal, hist


def atr(df: pd.DataFrame, length: int = 14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(length).mean()


def support_resistance(df: pd.DataFrame, lookback: int = 40):
    recent = df.tail(lookback)
    return float(recent["low"].min()), float(recent["high"].max())
