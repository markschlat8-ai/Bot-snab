import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# ===== НАСТРОЙКИ =====
TOKEN = "8746847826:AAHUj0sCz45t40ys1MYD-1JK5S29bUiAntU"
ADMIN_ID = 428332335

# ===== ОБЪЕКТЫ =====
OBJECTS = [
    "ЖК Лесной",
    "ЖК Центральный",
    "Школа №5",
    "Склад",
    "Офис",
    "ТЦ Восток"
]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_state = {}
request_id = 0


def get_objects_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=obj)] for obj in OBJECTS],
        resize_keyboard=True
    )


def get_status_kb(rid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟡 В работе", callback_data=f"work_{rid}")],
        [InlineKeyboardButton(text="🟢 Куплено", callback_data=f"done_{rid}")],
        [InlineKeyboardButton(text="🔴 Отмена", callback_data=f"cancel_{rid}")]
    ])


@dp.message(lambda msg: msg.text == "/start")
async def start(message: types.Message):
    user_state[message.from_user.id] = {}
    await message.answer("🏗 Выберите объект:", reply_markup=get_objects_kb())


@dp.message()
async def process(message: types.Message):
    global request_id

    user_id = message.from_user.id

    if user_id not in user_state:
        return

    data = user_state[user_id]

    if "object" not in data:
        data["object"] = message.text
        await message.answer("📦 Введите материал:")
        return

    if "material" not in data:
        data["material"] = message.text
        await message.answer("🔢 Введите количество:")
        return

    data["qty"] = message.text
    request_id += 1

    text = (
        f"📋 ЗАЯВКА №{request_id}\n\n"
        f"🏗 Объект: {data['object']}\n"
        f"📦 Материал: {data['material']}\n"
        f"🔢 Количество: {data['qty']}\n\n"
        f"📊 Статус: НОВАЯ"
    )

    await bot.send_message(ADMIN_ID, text, reply_markup=get_status_kb(request_id))
    await message.answer("✅ Заявка отправлена")

    user_state.pop(user_id)


@dp.callback_query()
async def callbacks(call: types.CallbackQuery):
    data = call.data

    if "work" in data:
        status = "🟡 В РАБОТЕ"
    elif "done" in data:
        status = "🟢 КУПЛЕНО"
    else:
        status = "🔴 ОТМЕНА"

    text_lines = call.message.text.split("\n")
    text_lines[-1] = f"📊 Статус: {status}"

    await call.message.edit_text("\n".join(text_lines))
    await call.answer("Обновлено")


async def main():
    # КЛЮЧЕВОЕ — убивает старые сессии
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
