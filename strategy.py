import pandas as pd
from bitget_api import fetch_ohlcv
from indicators import ema, rsi, macd, atr, support_resistance


def analyze_symbol(symbol: str):
    try:
        raw = fetch_ohlcv(symbol)
    except Exception as exc:
        return {"ok": False, "symbol": symbol, "error": str(exc)}

    if not raw:
        return {"ok": False, "symbol": symbol, "error": "無行情資料"}

    df = pd.DataFrame(raw, columns=["time", "open", "high", "low", "close", "volume"])
    close = df["close"].astype(float)
    price = float(close.iloc[-1])

    ema20 = float(ema(close, 20).iloc[-1])
    ema50 = float(ema(close, 50).iloc[-1])
    rsi14 = float(rsi(close, 14).iloc[-1])
    macd_line, macd_signal, macd_hist = macd(close)
    macd_now = float(macd_line.iloc[-1])
    macd_sig = float(macd_signal.iloc[-1])
    atr14 = float(atr(df, 14).iloc[-1])
    support, resistance = support_resistance(df)

    score = 50
    reasons = []

    if ema20 > ema50:
        direction = "做多"
        score += 18
        reasons.append("EMA20 > EMA50，短線偏多")
    else:
        direction = "做空"
        score -= 18
        reasons.append("EMA20 < EMA50，短線偏空")

    if macd_now > macd_sig:
        score += 14
        reasons.append("MACD 多方動能較強")
    else:
        score -= 14
        reasons.append("MACD 空方動能較強")

    if rsi14 < 30:
        score += 10
        reasons.append("RSI 低檔，可能反彈")
    elif rsi14 > 70:
        score -= 10
        reasons.append("RSI 高檔，追多風險升高")
    else:
        reasons.append("RSI 中性區間")

    if close.iloc[-1] > close.iloc[-2]:
        score += 4
    else:
        score -= 4

    score = max(0, min(100, int(score)))

    if direction == "做多":
        entry = price
        stop_loss = max(price - atr14 * 1.3, support)
        take_profit = price + atr14 * 2.0
    else:
        entry = price
        stop_loss = min(price + atr14 * 1.3, resistance)
        take_profit = price - atr14 * 2.0

    return {
        "ok": True,
        "symbol": symbol,
        "price": round(price, 4),
        "direction": direction,
        "score": score,
        "rsi": round(rsi14, 2),
        "macd": round(macd_now, 5),
        "ema20": round(ema20, 4),
        "ema50": round(ema50, 4),
        "atr": round(atr14, 4),
        "support": round(support, 4),
        "resistance": round(resistance, 4),
        "entry": round(entry, 4),
        "stop_loss": round(stop_loss, 4),
        "take_profit": round(take_profit, 4),
        "reasons": reasons,
    }
