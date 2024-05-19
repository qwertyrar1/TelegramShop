from aiogram import Router, F
from aiogram.types import (Message, InlineQuery,)
from settings import OrderStates
from aiogram.fsm.context import FSMContext
from bot.query_results import get_query_results

router = Router()


@router.message(OrderStates.choose_action, F.text == 'FAQ')
async def send_faq(message: Message):
    await message.answer(
        'Чтобы узнать ответы на часто задаваемые вопросы, напишите: @TestTaskShopBot и выберите вопрос из списка')


@router.inline_query(OrderStates.choose_action)
async def inline_faq(iquery: InlineQuery, state: FSMContext):
    await state.set_state(OrderStates.faq)
    await iquery.answer(get_query_results(), cache_time=1, is_personal=True)


@router.message(OrderStates.faq, F.text)
async def send_answer(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choose_action)
    if message.text == 'Текст Вопроса 1':
        await message.answer('Ответ 1')
    elif message.text == 'Текст Вопроса 2':
        await message.answer('Ответ 2')
    elif message.text == 'Текст Вопроса 3':
        await message.answer('Ответ 3')
    else:
        await message.answer('Пока что мы не можем ответить на ваш вопрос')
