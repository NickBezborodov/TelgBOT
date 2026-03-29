from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from handlers import register_handlers

TOKEN = "8626307956:AAE7_tLE8KwlNx6dCRxgNAkQdA9YhjkNxik"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == "__main__":
    print("Бот запущен")
    executor.start_polling(dp)