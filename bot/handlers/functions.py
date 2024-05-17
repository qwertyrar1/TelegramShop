from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, InlineKeyboardButton, \
    InlineKeyboardMarkup
from settings import OrderStates, IMAGE_PATH
from aiogram.fsm.context import FSMContext
from bot.keyboards import get_for_paginate_category_keyboard, get_for_paginate_subcategory_keyboard
from bot.actions import _get_products_by_subcategory

router = Router()


@router.message(OrderStates.choose_action, F.text == 'Каталог')
async def send_category(message: Message, state: FSMContext):
    await message.answer(text='Выберите категорию', reply_markup=await get_for_paginate_category_keyboard())
    await state.set_state(OrderStates.choose_category)


@router.message(OrderStates.get_amount, F.text)
async def get_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get('product_id')
    amount = int(message.text)
    await message.answer(text=f'product_id: {product_id}\nколичество: {amount}')


@router.callback_query(F.data.startswith('category_page_'))
async def paginate_category(call: CallbackQuery):
    page = int(call.data.split('_')[2])
    await call.message.edit_reply_markup(reply_markup=await get_for_paginate_category_keyboard(page))


@router.callback_query(F.data.startswith('subcategory_page_'))
async def paginate_subcategory(call: CallbackQuery):
    page = int(call.data.split('_')[3])
    category_id = call.data.split('_')[2]
    await call.message.edit_reply_markup(reply_markup=await get_for_paginate_subcategory_keyboard(page, category_id))


@router.callback_query(F.data.startswith('category_item_'))
async def handle_category_item(call: CallbackQuery, state: FSMContext):
    category_id = call.data.split('_')[2]
    await state.set_state(OrderStates.choose_subcategory)
    await call.message.answer(text='Выберите подкатегорию',
                              reply_markup=await get_for_paginate_subcategory_keyboard(category_id=category_id))


@router.callback_query(F.data.startswith('subcategory_item_'))
async def handle_subcategory_item(call: CallbackQuery, state: FSMContext):
    subcategory_name = call.data.split('_')[2]
    await state.set_state(OrderStates.show_products)
    products = await _get_products_by_subcategory(subcategory_name)
    for i in products:
        image = FSInputFile(IMAGE_PATH + i[0].image_path)
        add_cart_button = [[InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_cart_{i[0].id}')]]
        await call.message.answer_photo(photo=image, caption=i[0].description,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=add_cart_button))


@router.callback_query(F.data.startswith('add_cart_'))
async def add_to_cart(call: CallbackQuery, state: FSMContext):
    product_id = call.data.split('_')[2]
    await state.set_data(data={'product_id': product_id})
    await state.set_state(OrderStates.get_amount)
    await call.message.answer('Укажите количество товаров:')