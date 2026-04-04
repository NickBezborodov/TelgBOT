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
            await message.answer("📭 У тебя нет задач")
            return

        text = "📋 Твои задачи:\n\n"

        for i, task in enumerate(tasks, start=1):
            text += f"🔹 {i}. {task[1]}\n"

        await message.answer(text)

        # кнопки под каждой задачей
        for i, task in enumerate(tasks, start=1):
            task_id = task[0]

            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("✏️ Изменить", callback_data=f"edit_{task_id}"),
                InlineKeyboardButton("❌ Удалить", callback_data=f"delete_{task_id}")
            )

            await message.answer(f"Действия для задачи {i}", reply_markup=keyboard)


    @dp.callback_query_handler(lambda c: c.data.startswith("delete_"))
    async def delete_callback(callback_query: types.CallbackQuery):
        task_id = int(callback_query.data.split("_")[1])

        delete_task(task_id, callback_query.from_user.id)

        await callback_query.answer("Удалено")

        tasks = get_tasks(callback_query.from_user.id)

        if not tasks:
            await callback_query.message.answer("📭 У тебя нет задач")
            return

        text = "📋 Твои задачи:\n\n"

        for i, task in enumerate(tasks, start=1):
            text += f"🔹 {i}. {task[1]}\n"

        await callback_query.message.answer(text)


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
        
        
        @dp.callback_query_handler(lambda c: c.data.startswith("edit_"))
        async def edit_callback(callback_query: types.CallbackQuery):
            await callback_query.answer("Функция в разработке")
