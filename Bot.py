import asyncio
import os
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message()
async def handle(message: types.Message):
    user_id = message.from_user.id

    if message.text == "/start":
        user_data[user_id] = {}
        await message.answer("Введите объект:")
        return

    if user_id not in user_data:
        return

    data = user_data[user_id]

    if "object" not in data:
        data["object"] = message.text
        await message.answer("Что нужно купить?")
    elif "material" not in data:
        data["material"] = message.text
        await message.answer("Количество?")
    elif "qty" not in data:
        data["qty"] = message.text
        await message.answer("Когда нужно?")
    else:
        data["date"] = message.text

        text = (
            "НОВАЯ ЗАЯВКА\n\n"
            f"Объект: {data['object']}\n"
            f"Материал: {data['material']}\n"
            f"Количество: {data['qty']}\n"
            f"Срок: {data['date']}"
        )

        await bot.send_message(ADMIN_ID, text)
        await message.answer("Заявка отправлена")

        user_data.pop(user_id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
