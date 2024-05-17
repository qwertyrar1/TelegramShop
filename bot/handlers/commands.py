from settings import OrderStates
from aiogram import Router, Bot
from settings import FOLLOW_CHAT_ID
from bot.keyboards import get_choice_keyboard
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    '''
    user_channel_status = await bot.get_chat_member(chat_id=FOLLOW_CHAT_ID, user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await state.set_state(OrderStates.choose_action)
        await message.answer('Выбери действие:')
    else:
        await bot.send_message(message.from_user.id, f'Пожалуйста подпишитесь на канал {FOLLOW_CHAT_ID}')
    '''
    await state.set_state(OrderStates.choose_action)
    await message.answer('Выбери действие:', reply_markup=get_choice_keyboard())