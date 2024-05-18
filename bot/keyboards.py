from functools import cache
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from actions import _get_all_categories, _get_subcategories_by_category
from settings import ITEMS_PER_PAGE


@cache
def get_choice_keyboard():
    keyboard = [
        [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина'), KeyboardButton(text='FAQ')],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def get_for_paginate_category_keyboard(page: int = 0):
    start_index = page * int(ITEMS_PER_PAGE)
    end_index = start_index + int(ITEMS_PER_PAGE)

    categories = [i[0] for i in await _get_all_categories()]
    paginated_categories = categories[start_index:end_index]

    buttons = [[InlineKeyboardButton(text=i.name, callback_data='category_item_' + str(i.id))]
               for i in paginated_categories]
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"category_page_{page - 1}"))
    if end_index < len(categories):
        navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"category_page_{page + 1}"))
    buttons.append(navigation_buttons)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_for_paginate_subcategory_keyboard(page: int = 0, category_id: str = None):
    start_index = page * int(ITEMS_PER_PAGE)
    end_index = start_index + int(ITEMS_PER_PAGE)

    subcategories = [i[0] for i in await _get_subcategories_by_category(category_id)]
    paginated_subcategories = subcategories[start_index:end_index]

    buttons = [[InlineKeyboardButton(text=i.name, callback_data='subcategory_item_' + str(i.name))]
               for i in paginated_subcategories]
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"subcategory_page_{category_id}_{page - 1}"))
    if end_index < len(subcategories):
        navigation_buttons.append(
            InlineKeyboardButton(text="Вперед ➡️", callback_data=f"subcategory_page_{category_id}_{page + 1}"))
    buttons.append(navigation_buttons)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
