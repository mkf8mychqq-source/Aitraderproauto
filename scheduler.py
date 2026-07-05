import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from config import settings
from telegram_bot import send_message
from reporter import build_market_report
from news_service import build_news_summary


async def safe_push(reason: str):
    try:
        report = build_market_report(reason)
        print(report)
        await send_message(report)
    except Exception as exc:
        err = f"❌ AI Trader Pro 執行錯誤：{exc}"
        print(err)
        await send_message(err)


async def run_forever():
    tz = ZoneInfo(settings.timezone)
    await safe_push("系統啟動")

    last_report_minute = None
    sent_daily = set()
    last_news_minute = None

    while True:
        now = datetime.now(tz)
        minute_key = now.strftime("%Y-%m-%d %H:%M")

        # 每 N 分鐘完整戰情室推播
        if now.minute % settings.report_interval_minutes == 0 and last_report_minute != minute_key:
            last_report_minute = minute_key
            await safe_push(f"每 {settings.report_interval_minutes} 分鐘定時更新")

        # 每日固定時間推播
        hm = now.strftime("%H:%M")
        day_key = now.strftime("%Y-%m-%d")
        for target in settings.daily_report_times:
            key = f"{day_key}-{target}"
            if hm == target and key not in sent_daily:
                sent_daily.add(key)
                await safe_push(f"每日固定戰情室 {target}")

        # 每 N 分鐘新聞掃描，只在偵測到關鍵風險字才簡短推播
        if now.minute % settings.news_check_interval_minutes == 0 and last_news_minute != minute_key:
            last_news_minute = minute_key
            summary = build_news_summary()
            risk_words = ["attack", "war", "iran", "hormuz", "fed", "cpi", "opec", "eia", "bitcoin", "etf"]
            if any(w in summary.lower() for w in risk_words):
                await send_message("🚨 新聞監控\n" + summary[:3200])

        await asyncio.sleep(20)
