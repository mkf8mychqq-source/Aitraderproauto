import ccxt
from config import settings


def create_exchange():
    return ccxt.bitget({
        "apiKey": settings.bitget_api_key,
        "secret": settings.bitget_secret,
        "password": settings.bitget_passphrase,
        "enableRateLimit": True,
        "options": {"defaultType": "swap"},
    })

exchange = create_exchange()


def normalize_symbol(symbol: str) -> str:
    # Bitget/CCXT 通常接受 BTC/USDT，也保留你指定的 XAUUSDT、CLUSDT 嘗試。
    return symbol.strip()


def fetch_ohlcv(symbol: str, timeframe: str = "15m", limit: int = 160):
    return exchange.fetch_ohlcv(normalize_symbol(symbol), timeframe=timeframe, limit=limit)


def fetch_balance_safe():
    try:
        return exchange.fetch_balance()
    except Exception as exc:
        return {"error": str(exc)}
