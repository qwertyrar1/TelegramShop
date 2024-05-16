import uuid

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(String, nullable=False)
    orders = relationship("Order", back_populates="client")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_path = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    subcategory = Column(String, ForeignKey("subcategories.name"))


class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    subcategories = relationship("Subcategory", back_populates="category")


class Subcategory(Base):
    __tablename__ = "subcategories"
    name = Column(String, nullable=False, primary_key=True)
    category_id = Column(UUID, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="subcategories")


class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart = Column(ARRAY(String), nullable=False)
    client_id = Column(UUID, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="orders")
    delivery_address = Column(String, nullable=False)


