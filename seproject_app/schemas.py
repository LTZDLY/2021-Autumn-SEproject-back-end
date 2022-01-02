from typing import List, Optional

from pydantic import BaseModel


class DishBase(BaseModel):
    describe: str
    description: Optional[str] = None
    flavor: Optional[str] = None
    price: float
    icon: Optional[str] = None


class DishCreate(DishBase):
    # store_id: int # 创建订单的菜品不需要商家id，因为创建菜品的商家唯一确定
    pass


class Dish(DishBase):
    id: int
    store_id: int

    class Config:
        orm_mode = True


class ShopBase(BaseModel):
    name: str
    phone: str
    describe: Optional[str] = None
    address: Optional[str] = None
    icon: Optional[str] = None


class ShopCreate(ShopBase):
    password: str


class Shop(ShopBase):
    id: int
    # is_active: bool
    # items: List[Dish] = []

    class Config:
        orm_mode = True
