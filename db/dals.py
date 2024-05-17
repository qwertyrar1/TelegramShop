from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Client, Category, Subcategory, Product, Order


class ClientDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_client(self, tg_id: str) -> Client:
        new_client = Client(tg_id=tg_id)
        self.db_session.add(new_client)
        await self.db_session.flush()
        return new_client


class OrderDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_order(self, cart: List, client_id: UUID, delivery_address: str) -> Order:
        new_order = Order(cart=cart, delivery_address=delivery_address)
        client = await self.db_session.get(Client, client_id)
        new_order.client = client
        self.db_session.add(new_order)
        await self.db_session.commit()
        return new_order


class CategoryDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_categories(self):
        query = select(Category)
        res = await self.db_session.execute(query)
        category_row = res.fetchall()
        return category_row


class SubcategoryDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_subcategories_by_category(self, category_id: UUID):
        query = select(Subcategory).where(Subcategory.category_id == category_id)
        res = await self.db_session.execute(query)
        subcategory_row = res.fetchall()
        return subcategory_row


class ProductDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_products_by_subcategory(self, subcategory_name: str):
        query = select(Product).where(Product.subcategory == subcategory_name)
        res = await self.db_session.execute(query)
        product_row = res.fetchall()
        return product_row

    async def get_products_by_id(self, product_id: str):
        query = select(Product).where(Product.id == product_id)
        res = await self.db_session.execute(query)
        product_row = res.fetchall()
        return product_row
