from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, \
    InlineKeyboardMarkup
from settings import OrderStates, IMAGE_PATH, EXCEL_FILE_PATH
from aiogram.fsm.context import FSMContext
from bot.actions import _get_product_by_id, _create_new_order, _get_client_by_tg_id
from pay import create_payment, payment_check
from work_with_excel import add_to_excel
import uuid

router = Router()


@router.message(OrderStates.choose_action, F.text == 'Корзина')
async def send_products_from_cart(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        for item in data.get('cart'):
            product = await _get_product_by_id(uuid.UUID(item[0]))
            image = FSInputFile(IMAGE_PATH + product.image_path)
            delete_cart_button = [
                [InlineKeyboardButton(text='Удалить из корзины', callback_data=f'delete_cart_{product.id}')]]
            await message.answer_photo(photo=image, caption=f'{product.description}\nКоличество: {item[1]}',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=delete_cart_button))
        order_button = [[InlineKeyboardButton(text='Заказать', callback_data='order')]]
        await message.answer(text='Сделать заказ', reply_markup=InlineKeyboardMarkup(inline_keyboard=order_button))
    except:
        await message.answer('Корзина пуста')


@router.message(OrderStates.get_address, F.text)
async def create_order(message: Message, state: FSMContext):
    await state.set_state(OrderStates.create_order)
    data = await state.get_data()
    client = await _get_client_by_tg_id(str(message.from_user.id))
    await state.update_data(data={'client': client, 'pay_text': message.text})
    cart = [[i[0], str(i[1])] for i in data.get('cart')]
    price = 0
    for i in cart:
        product = await _get_product_by_id(i[0])
        price += product.price * int(i[1])
    url, payment = create_payment(price)
    await state.update_data(data={'payment': payment})
    pay_button = [[InlineKeyboardButton(text='Оплатить', url=url),
                   InlineKeyboardButton(text='Подтвердить оплату', callback_data='complete_payment')]]
    await message.answer('Ссылка на платеж:', reply_markup=InlineKeyboardMarkup(inline_keyboard=pay_button))


@router.callback_query(F.data.startswith('delete_cart_'))
async def delete_from_cart(call: CallbackQuery, state: FSMContext):
    product_id = call.data.split('_')[2]
    data = await state.get_data()
    cart = data.get('cart')
    for item in cart[:]:
        if product_id == item[0]:
            cart.remove(item)
    await state.update_data(data={'cart': cart})
    await call.message.answer('Товар удален')


@router.callback_query(F.data.startswith('order'))
async def get_address(call: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.get_address)
    data = await state.get_data()
    if len(data.get('cart')) > 0:
        await call.message.answer('Укажите адрес доставки')
    else:
        await state.set_state(OrderStates.choose_action)
        await call.message.answer('Корзина пуста')


@router.callback_query(OrderStates.create_order, F.data.startswith('complete_payment'))
async def approve_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment = data.get('payment')
    if payment_check(payment.id):
        client = data.get('client')
        cart = [[i[0], str(i[1])] for i in data.get('cart')]
        price = 0
        for i in cart:
            product = await _get_product_by_id(i[0])
            price += product.price * int(i[1])
        order = await _create_new_order(cart, str(client[0][0].id), data.get('pay_text'))
        add_to_excel(EXCEL_FILE_PATH, [str(order.id)])
        await state.update_data(data={'unconfirmed_cart': [], 'cart': []})
        await state.set_state(OrderStates.choose_action)
        await call.message.answer('Платеж прошел успешно')
    else:
        await call.message.answer('Ошибка')
