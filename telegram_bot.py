from telegram import Bot
from config import settings

_bot = Bot(token=settings.telegram_token)

async def send_message(text: str):
    if not settings.telegram_token or not settings.chat_id:
        print("Telegram 尚未設定，訊息只印在終端機。")
        print(text)
        return
    await _bot.send_message(chat_id=settings.chat_id, text=text[:3900])
