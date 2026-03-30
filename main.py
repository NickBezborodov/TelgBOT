from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from handlers import register_handlers
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == "__main__":
    print("Бот запущен")
    executor.start_polling(dp)