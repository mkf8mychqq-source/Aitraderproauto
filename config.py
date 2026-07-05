import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _bool(name: str, default: bool = False) -> bool:
    value = _env(name, str(default)).lower()
    return value in {"1", "true", "yes", "y", "on"}


@dataclass
class Settings:
    telegram_token: str = _env("TELEGRAM_TOKEN")
    chat_id: str = _env("CHAT_ID")
    bitget_api_key: str = _env("BITGET_API_KEY")
    bitget_secret: str = _env("BITGET_SECRET")
    bitget_passphrase: str = _env("BITGET_PASSPHRASE")
    report_interval_minutes: int = int(_env("REPORT_INTERVAL_MINUTES", "5") or 5)
    news_check_interval_minutes: int = int(_env("NEWS_CHECK_INTERVAL_MINUTES", "1") or 1)
    daily_report_times: list[str] = None
    timezone: str = _env("TIMEZONE", "Asia/Taipei")
    symbols: list[str] = None
    enable_auto_trade: bool = _bool("ENABLE_AUTO_TRADE", False)

    def __post_init__(self):
        self.daily_report_times = [x.strip() for x in _env("DAILY_REPORT_TIMES", "06:00,21:00").split(",") if x.strip()]
        self.symbols = [x.strip() for x in _env("SYMBOLS", "BTC/USDT,ETH/USDT,XAUUSDT,CLUSDT").split(",") if x.strip()]


settings = Settings()
