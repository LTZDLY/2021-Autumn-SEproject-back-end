from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, nullable=False)
    open_id = Column(String, index=True, nullable=False)

    # items = relationship("Item", back_populates="owner")


class Shop(Base):
    __tablename__ = "store"

    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, nullable=False)
    name = Column(String)
    phone = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    describe = Column(String)
    address = Column(String)
    distance = Column(Integer)
    img = Column(String)

    # owner = relationship("User", back_populates="items")


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, nullable=False)
    store_id = Column(Integer, nullable=False)
    describe = Column(String)
    flavor = Column(String)
    price = Column(Float)
    description = Column(String)
    icon = Column(String)
