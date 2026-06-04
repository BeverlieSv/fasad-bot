import os
import re
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

PROFILE = 400
HANDLE = 450
GLASS = 1100
WASTE = 1.2

UPHOLSTER = 60
ANGLE = 90
SCREW = 1
HINGE_PRICE = 85
HINGE_SCREW = 2
CUT = 200
HINGE_HOLE = 50
ASSEMBLY = 300


def parse(text):
    text = text.lower()

    size = re.findall(r"(\d+)\s*[xх]\s*(\d+)", text)
    if not size:
        return None

    w, h = map(float, size[0])

    qty = 1
    q = re.findall(r"(\d+)\s*шт", text)
    if q:
        qty = int(q[0])

    hinges = 0
    hq = re.findall(r"(\d+)\s*пет", text)
    if hq:
        hinges = int(hq[0])

    handle = True
    if "без руч" in text:
        handle = False

    return w, h, qty, hinges, handle


def calc(w, h, qty, hinges, handle):
    perim = 2 * (w + h) / 1000
    area = (w * h) / 1_000_000

    glass = area * WASTE * GLASS
    seal = perim * UPHOLSTER

    if handle:
        profile = (h / 1000) * HANDLE + (perim - h / 1000) * PROFILE
    else:
        profile = perim * PROFILE

    hardware = (4 * ANGLE) + (16 * SCREW)

    hinges_cost = hinges * HINGE_PRICE
    hinge_screws = hinges * HINGE_SCREW

    work = CUT + (hinges * HINGE_HOLE) + ASSEMBLY

    one = glass + seal + profile + hardware + hinges_cost + hinge_screws + work

    return one, one * qty


@dp.message()
async def handler(message: Message):
    data = parse(message.text)

    if not data:
        await message.answer("❌ Формат: 2410x480 2шт 5 петель")
        return

    w, h, qty, hinges, handle = data
    one, total = calc(w, h, qty, hinges, handle)

    await message.answer(
        f"""📦 ФАСАД

📏 {w} x {h}
📦 {qty} шт
🪛 {hinges} петель

💰 1 шт: {round(one,2)}
💰 ИТОГО: {round(total,2)}"""
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())    w, h = map(float, size[0])

    qty = 1
    q = re.findall(r"(\d+)\s*шт", text)
    if q:
        qty = int(q[0])

    hinges = 0
    hq = re.findall(r"(\d+)\s*пет", text)
    if hq:
        hinges = int(hq[0])

    handle = True
    if "без руч" in text:
        handle = False

    return w, h, qty, hinges, handle


def calc(w, h, qty, hinges, handle):
    perim = 2 * (w + h) / 1000
    area = (w * h) / 1_000_000

    glass = area * WASTE * GLASS
    seal = perim * UPHOLSTER

    if handle:
        profile = (h / 1000) * HANDLE + (perim - h / 1000) * PROFILE
    else:
        profile = perim * PROFILE

    hardware = (4 * ANGLE) + (16 * SCREW)

    hinges_cost = hinges * HINGE_PRICE
    hinge_screws = hinges * HINGE_SCREW

    work = CUT + (hinges * HINGE_HOLE) + ASSEMBLY

    one = glass + seal + profile + hardware + hinges_cost + hinge_screws + work

    return one, one * qty


@dp.message()
async def handler(message: types.Message):
    data = parse(message.text)

    if not data:
        await message.answer("❌ Формат: 2410x480 2шт 5 петель")
        return

    w, h, qty, hinges, handle = data
    one, total = calc(w, h, qty, hinges, handle)

    await message.answer(
        f"""📦 ФАСАД КАЛЬКУЛЯТОР

📏 {w} x {h}
📦 {qty} шт
🪛 {hinges} петель
🚪 Ручка: {"Да" if handle else "Нет"}

💰 1 шт: {round(one,2)} сом
💰 ИТОГО: {round(total,2)} сом"""
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())    qty_match = re.findall(r"(\d+)\s*шт", text)
    if qty_match:
        qty = int(qty_match[0])

    # петли
    hinges = 0
    hinge_match = re.findall(r"(\d+)\s*пет", text)
    if hinge_match:
        hinges = int(hinge_match[0])

    # ручка
    handle = True
    if "без руч" in text:
        handle = False

    return w, h, qty, hinges, handle


def calc(w, h, qty, hinges, handle):
    perim = 2 * (w + h) / 1000
    area = (w * h) / 1_000_000

    glass = area * WASTE * GLASS
    seal = perim * UPHOLSTER

    # профиль
    if handle:
        profile = (h/1000) * HANDLE + (perim - h/1000) * PROFILE
    else:
        profile = perim * PROFILE

    hardware = (4 * ANGLE) + (16 * SCREW)

    hinges_cost = hinges * HINGE_PRICE
    hinge_screws = hinges * HINGE_SCREW

    work = CUT + (hinges * HINGE_HOLE) + ASSEMBLY

    one = glass + seal + profile + hardware + hinges_cost + hinge_screws + work

    return one, one * qty


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    data = parse(text)

    if not data:
        await update.message.reply_text(
            "❌ Не понял формат\nПример: 2410x480 2шт 5 петель"
        )
        return

    w, h, qty, hinges, handle = data

    one, total = calc(w, h, qty, hinges, handle)

    await update.message.reply_text(
        f"""📦 ФАСАД РАСЧЁТ

📏 Размер: {w} x {h}
📦 Кол-во: {qty}
🪛 Петли: {hinges}
🚪 Ручка: {"Да" if handle else "Нет"}

💰 1 шт: {round(one, 2)} сом
💰 ВСЕГО: {round(total, 2)} сом"""
    )


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handler))

app.run_polling()
