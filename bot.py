import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8746847826:AAFFbv7P7eqigBS8vYDu36KN-FtSYy4X9cg"
ADMIN_ID = 428332335

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
request_id = 0

def get_kb(rid):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В работе", callback_data=f"work_{rid}")],
        [InlineKeyboardButton(text="Куплено", callback_data=f"done_{rid}")],
        [InlineKeyboardButton(text="Отмена", callback_data=f"cancel_{rid}")]
    ])
    return kb

@dp.message()
async def handle(message: types.Message):
    global request_id
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
        data["qty"] = message.text
        request_id += 1

        text = (
            f"ЗАЯВКА #{request_id}\n\n"
            f"Объект: {data['object']}\n"
            f"Материал: {data['material']}\n"
            f"Количество: {data['qty']}\n"
            f"Статус: НОВАЯ"
        )

        await bot.send_message(ADMIN_ID, text, reply_markup=get_kb(request_id))
        await message.answer("Заявка отправлена")

        user_data.pop(user_id)

@dp.callback_query()
async def callback(call: types.CallbackQuery):
    data = call.data

    if "work" in data:
        status = "В РАБОТЕ"
    elif "done" in data:
        status = "КУПЛЕНО"
    else:
        status = "ОТМЕНА"

    text = call.message.text.split("\n")
    text[-1] = f"Статус: {status}"

    await call.message.edit_text("\n".join(text))
    await call.answer("Статус обновлен")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
