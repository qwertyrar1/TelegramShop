from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, InlineKeyboardButton, \
    InlineKeyboardMarkup
from settings import OrderStates, IMAGE_PATH
from aiogram.fsm.context import FSMContext
from bot.keyboards import get_for_paginate_category_keyboard, get_for_paginate_subcategory_keyboard, get_choice_keyboard
from bot.actions import _get_products_by_subcategory

router = Router()


@router.message(OrderStates.choose_action, F.text == 'Каталог')
async def send_category(message: Message, state: FSMContext):
    keyboard = await get_for_paginate_category_keyboard()
    await message.answer(text='Выберите категорию', reply_markup=ReplyKeyboardRemove())
    await message.answer(text='Категории', reply_markup=keyboard)
    data = await state.get_data()
    if len(data) == 0:
        await state.update_data(data={'unconfirmed_cart': [], 'cart': []})
    await state.set_state(OrderStates.choose_category)


@router.message(OrderStates.get_amount, F.text)
async def get_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get('product_id')
    amount = int(message.text)
    data.get('unconfirmed_cart').append([product_id, amount])
    await state.update_data(data=data)
    confirm_cart_button = [[InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_cart')]]
    await message.answer('Добавить выбранные товары в корзину?',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=confirm_cart_button))


@router.callback_query(F.data.startswith('category_page_'))
async def paginate_category(call: CallbackQuery):
    page = int(call.data.split('_')[2])
    keyboard = await get_for_paginate_category_keyboard(page)
    await call.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith('subcategory_page_'))
async def paginate_subcategory(call: CallbackQuery):
    page = int(call.data.split('_')[3])
    category_id = call.data.split('_')[2]
    keyboard = await get_for_paginate_subcategory_keyboard(page, category_id)
    await call.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith('category_item_'))
async def handle_category_item(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split('_')[2]
    await state.set_state(OrderStates.choose_subcategory)
    keyboard = await get_for_paginate_subcategory_keyboard(category_id=category_id)
    await call.message.answer(text='Выберите подкатегорию',
                              reply_markup=keyboard)


@router.callback_query(F.data.startswith('subcategory_item_'))
async def handle_subcategory_item(call: CallbackQuery, state: FSMContext):
    subcategory_name = call.data.split('_')[2]
    await state.set_state(OrderStates.show_products)
    products = await _get_products_by_subcategory(subcategory_name)
    for i in products:
        image = FSInputFile(IMAGE_PATH + i[0].image_path)
        add_cart_button = [[InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_cart_{i[0].id}')]]
        await call.message.answer_photo(photo=image, caption=f'{i[0].description}\nЦена: {i[0].price}',
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=add_cart_button))


@router.callback_query(F.data.startswith('add_cart_'))
async def add_to_cart(call: CallbackQuery, state: FSMContext):
    product_id = call.data.split('_')[2]
    await state.update_data(data={'product_id': product_id})
    await state.set_state(OrderStates.get_amount)
    await call.message.answer('Укажите количество товаров:')


@router.callback_query(OrderStates.get_amount, F.data.startswith('confirm_cart'))
async def confirm_cart(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_in_cart = False
    for item in data.get('unconfirmed_cart'):
        for cart_item in data.get('cart'):
            if cart_item[0] == item[0]:
                cart_item[1] += item[1]
                item_in_cart = True
                break
        if not item_in_cart:
            data.get('cart').append(item)
    await state.update_data(data={'unconfirmed_cart': [], 'cart': data.get('cart'), 'product_id': ''})
    await call.message.answer('Товары добавлены в корзину', reply_markup=get_choice_keyboard())
    await state.set_state(OrderStates.choose_action)

