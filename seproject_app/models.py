from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.schema import Table

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    open_id = Column(String, index=True, nullable=False)

    # items = relationship("Item", back_populates="owner")


class Shop(Base):
    __tablename__ = "store"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    name = Column(String)
    phone = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    describe = Column(String)
    address = Column(String)
    distance = Column(Integer, default=0)
    img = Column(String)

    # owner = relationship("User", back_populates="items")


class Order_Dish(Base):
    __tablename__ = "order-dish"

    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True, nullable=False)
    dish_id = Column(Integer, ForeignKey("dish.id"), primary_key=True, nullable=False)
    num = Column(Integer, nullable=False)


class Dish(Base):
    __tablename__ = "dish"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    store_id = Column(Integer, ForeignKey("store.id"), nullable=False)
    describe = Column(String)
    flavor = Column(String)
    price = Column(Float)
    description = Column(String)
    icon = Column(String)


class Comment(Base):
    __tablename__ = "evaluate"

    order_id = Column(
        Integer, ForeignKey("order.id"), primary_key=True, index=True, nullable=False
    )
    user_text = Column(String)
    store_text = Column(String)
    user_time = Column(DateTime)
    store_time = Column(DateTime)
    user_score = Column(Integer)


class Order(Base):
    __tablename__ = "order"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    store_id = Column(Integer, ForeignKey("store.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    price = Column(Float, nullable=False)


class Order_Status(Base):
    __tablename__ = "order_status"

    order_id = Column(
        Integer, ForeignKey("order.id"), primary_key=True, index=True, nullable=False
    )
    submit_time = Column(DateTime)
    finish_time = Column(DateTime)
    status = Column(Boolean, default=False)
    comment = Column(Boolean, default=False)
