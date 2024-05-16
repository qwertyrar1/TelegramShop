from db.session import async_session
from db.dals import ClientDAL, OrderDAL, ProductDAL, CategoryDAL, SubcategoryDAL
import uuid


async def _create_new_client(tg_id):
    async with async_session() as session:
        async with session.begin():
            client_dal = ClientDAL(session)
            book = await client_dal.create_client(tg_id=tg_id)
            return book.tg_id


async def _create_new_order(cart, client_id, delivery_address):
    async with async_session() as session:
        async with session.begin():
            order_dal = OrderDAL(session)
            order = await order_dal.create_order(cart=cart, client_id=uuid.UUID(client_id),
                                                 delivery_address=delivery_address)
            return order


async def _get_all_categories():
    async with async_session() as session:
        async with session.begin():
            category_dal = CategoryDAL(session)
            categories = await category_dal.get_all_categories()
            return categories


async def _get_subcategories_by_category(category_id):
    async with async_session() as session:
        async with session.begin():
            subcategory_dal = SubcategoryDAL(session)
            subcategories = await subcategory_dal.get_subcategories_by_category(category_id=uuid.UUID(category_id))
            return subcategories


async def _get_products_by_subcategory(subcategory_name):
    async with async_session() as session:
        async with session.begin():
            product_dal = ProductDAL(session)
            products = await product_dal.get_products_by_subcategory(subcategory_name=subcategory_name)
            return products
