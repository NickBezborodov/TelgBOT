    from aiogram import types
from db import add_task, get_tasks, delete_task, update_task
import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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

        for i, task in enumerate(tasks, start=1):
            task_id = task[0]
            task_text = task[1]

            keyboard = InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text="❌ Удалить",
                callback_data=f"delete_{task_id}"
            )
            keyboard.add(button)

            await message.answer(f"{i}. {task_text}", reply_markup=keyboard)


     @dp.callback_query_handler(lambda c: c.data.startswith("delete_"))
     async def delete_callback(callback_query: types.CallbackQuery):
        task_id = int(callback_query.data.split("_")[1])

        delete_task(task_id, callback_query.from_user.id)

        await callback_query.answer("Удалено")
        await callback_query.message.delete()


    @dp.message_handler(commands=["delete"])
    async def delete_handler(message: types.Message):
        try:
            index = int(message.text.split()[1])
        except:
            await message.answer("Используй: /delete номер")
            return

        tasks = get_tasks(message.from_user.id)

        if index < 1 or index > len(tasks):
            await message.answer("Такой задачи нет")
            return

        task_id = tasks[index - 1][0]  # ВАЖНО
        delete_task(task_id, message.from_user.id)

        await message.answer("Удалено")