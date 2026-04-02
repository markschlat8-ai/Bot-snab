import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "8746847826:AAFFbv7P7eqigBS8vYDu36KN-FtSYy4X9cg"
ADMIN_ID = 428332335

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
        await message.answer("Введите материал:")
    elif "material" not in data:
        data["material"] = message.text
        await message.answer("Введите количество:")
    else:
        text = f"Заявка:\nОбъект: {data['object']}\nМатериал: {data['material']}\nКоличество: {message.text}"
        await bot.send_message(ADMIN_ID, text)
        await message.answer("Заявка отправлена ✅")
        user_data.pop(user_id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
