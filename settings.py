import os
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
IMAGE_PATH = os.getenv("IMAGE_PATH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FOLLOW_CHAT_ID = os.getenv("FOLLOW_CHAT_ID")
ITEMS_PER_PAGE = os.getenv("ITEMS_PER_PAGE")
YOOKASSA_API_KEY = os.getenv("YOOKASSA_API_KEY")
YOOKASSA_API_ID = os.getenv("YOOKASSA_API_ID")
BOT_LINK = os.getenv("BOT_LINK")


class OrderStates(StatesGroup):
    choose_action = State()
    choose_category = State()
    choose_subcategory = State()
    show_products = State()
    get_amount = State()
    get_address = State()
    create_order = State()
    faq = State()
