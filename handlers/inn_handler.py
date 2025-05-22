import requests
from datetime import datetime
from aiogram.types import Message
from config import DADATA_TOKEN, DADATA_URL

async def handle_inn(message: Message):
    inn = message.text.strip()
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

            # Обработка даты регистрации
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
