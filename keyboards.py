from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Список континентов
continents = ["Africa", "Asia", "Europe", "America", "Australia"]


# Клавиатура с континентами
async def continents_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in continents:
        keyboard.add(
            InlineKeyboardButton(
                text=key,
                callback_data=f"continent_{key.lower().replace(' ', '_')}"
            )
        )
    return keyboard.adjust(2).as_markup()


# Страны по континентам (обновлённые)
countries_by_continent = {
    "africa": [
        "South Africa", "Morocco", "Nigeria", "Botswana"
    ],
    "asia": [
        "Macau", "Philippines", "Singapore", "South Korea", "Vietnam",
        "Cambodia", "Malaysia", "Nepal", "Georgia", "Armenia", "Kazakhstan"
    ],
    "europe": [
        "Monaco", "France", "Germany", "United Kingdom", "Spain", "Italy",
        "Austria", "Netherlands", "Switzerland", "Czech Republic", "Estonia", "Belarus"
    ],
    "america": [
        "United States", "Canada", "Mexico", "Argentina", "Uruguay",
        "Chile", "Colombia", "Dominican Republic", "Bahamas", "Puerto Rico",
        "Panama", "Costa Rica"
    ],
    "australia": [
        "Australia", "New Zealand", "Samoa"
    ]
}


# Клавиатура со странами и кнопкой "🔙 Back"
async def countries_keyboard(continent_key: str):
    keyboard = InlineKeyboardBuilder()
    countries = countries_by_continent.get(continent_key, [])

    for country in countries:
        keyboard.add(
            InlineKeyboardButton(
                text=country,
                callback_data=f"country_{country.lower().replace(' ', '_')}"
            )
        )

    # Кнопка "Back" — в отдельной строке
    keyboard.adjust(2)
    keyboard.row(
        InlineKeyboardButton(
            text="🔙 Back",
            callback_data="back_to_continents"
        )
    )

    return keyboard.as_markup()

