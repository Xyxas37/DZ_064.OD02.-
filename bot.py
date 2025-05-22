import asyncio
import requests
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from config import BOT_TOKEN, DADATA_TOKEN, DADATA_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def handle_inn(message: Message):
    inn = message.text.strip()
    if not inn.isdigit():
        await message.answer("Введите корректный ИНН (только цифры).")
        return

    headers = {
        "Authorization": f"Token {DADATA_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"query": inn}

    try:
        response = requests.post(DADATA_URL, json=data, headers=headers)
        response.raise_for_status()

        suggestions = response.json().get("suggestions", [])
        if suggestions:
            info = suggestions[0]["data"]
            name = info.get("name", {}).get("full_with_opf", "—")
            ogrn = info.get("ogrn", "—")
            address = info.get("address", {}).get("value", "—")
            status = info.get("state", {}).get("status", "—")


            timestamp = info.get("state", {}).get("registration_date")
            if timestamp:
                reg_date = datetime.fromtimestamp(timestamp / 1000).strftime("%d.%m.%Y")
            else:
                reg_date = "—"

            reply = (
                f"{name}\n"
                f"ИНН: {inn}\n"
                f"ОГРН: {ogrn}\n"
                f"Адрес: {address}\n"
                f"Дата регистрации: {reg_date}\n"
                f"Статус: {status}"
            )
        else:
            reply = "Организация с таким ИНН не найдена."

    except Exception as e:
        reply = f"Ошибка при запросе: {str(e)}"

    await message.answer(reply)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
