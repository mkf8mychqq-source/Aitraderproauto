from config import settings
from strategy import analyze_symbol
from news_service import build_news_summary


def build_market_report(reason: str = "定時更新") -> str:
    lines = [f"📊 AI Trader Pro 全自動戰情室", f"觸發：{reason}", ""]

    for symbol in settings.symbols:
        r = analyze_symbol(symbol)
        if not r.get("ok"):
            lines += [f"{symbol}", f"狀態：❌ {r.get('error')}", "----------------------"]
            continue
        lines += [
            f"{r['symbol']}",
            f"價格：{r['price']}",
            f"方向：{r['direction']}",
            f"勝率評分：{r['score']} / 100",
            f"RSI：{r['rsi']}｜MACD：{r['macd']}",
            f"EMA20：{r['ema20']}｜EMA50：{r['ema50']}",
            f"支撐：{r['support']}｜壓力：{r['resistance']}",
            f"進場：{r['entry']}",
            f"停損：{r['stop_loss']}",
            f"停利：{r['take_profit']}",
            "理由：" + "；".join(r["reasons"][:3]),
            "----------------------",
        ]

    lines += ["", build_news_summary()]
    if not settings.enable_auto_trade:
        lines += ["", "⚠️ 自動下單：關閉。此版本只推播，不會下單。"]
    return "\n".join(lines)
