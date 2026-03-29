from aiogram import types
from db import add_task, get_tasks, delete_task, update_task
import requests


def register_handlers(dp):

    @dp.message_handler(commands=["start"])
    async def start_handler(message: types.Message):
        await message.answer("Бот работает")


    @dp.message_handler(commands=["add"])
    async def add_handler(message: types.Message):
        text = message.get_args()

        if not text:
            await message.answer("Пример: /add купить хлеб")
            return

        add_task(message.from_user.id, text)
        await message.answer(f"Добавлено: {text}")

        
    @dp.message_handler(commands=["quote"])
    async def quote_handler(message: types.Message):
        try:
            response = requests.get("https://api.quotable.io/random")
            data = response.json()

            quote = data.get("content")
            author = data.get("author")

            await message.answer(f"{quote}\n\n— {author}")

        except Exception:
            await message.answer("Ошибка при получении цитаты")

    @dp.message_handler(commands=["update"])
    async def update_handler(message: types.Message):
        args = message.get_args()

        if not args:
            await message.answer("Пример: /update 1 новый текст")
            return

        parts = args.split(maxsplit=1)

        if len(parts) < 2 or not parts[0].isdigit():
            await message.answer("Пример: /update 1 новый текст")
            return

        task_id = int(parts[0])
        new_text = parts[1]

        update_task(task_id, message.from_user.id, new_text)
        await message.answer("Задача обновлена")


    @dp.message_handler(commands=["list"])
    async def list_handler(message: types.Message):
        tasks = get_tasks(message.from_user.id)

        if not tasks:
            await message.answer("У тебя нет задач")
            return

        text = "📋 Твои задачи:\n\n"

        for task in tasks:
            text += f"🔹 {task[0]}: {task[1]}\n"

        await message.answer(text)


    @dp.message_handler(commands=["delete"])
    async def delete_handler(message: types.Message):
        args = message.get_args()

        if not args or not args.isdigit():
            await message.answer("Пример: /delete 1")
            return

        delete_task(int(args), message.from_user.id)
        await message.answer("Удалено")