from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class DishBase(BaseModel):
    describe: str  # 菜品名
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


class DishOrder(BaseModel):
    id: int
    num: int


class ShopLogin(BaseModel):
    phone: str
    password: str


class ShopBase(BaseModel):
    name: str
    phone: str
    describe: Optional[str] = None
    address: Optional[str] = None
    img: Optional[str] = None


class ShopCreate(ShopBase):
    password: str


class Shop(ShopBase):
    id: int
    # is_active: bool
    # items: List[Dish] = []

    class Config:
        orm_mode = True


class ShopChange(BaseModel):
    name: str
    password: str
    describe: Optional[str] = None
    address: Optional[str] = None
    img: Optional[str] = None


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    openid: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    store_id: int
    totalPrice: int


class OrderCreate(OrderBase):
    id: int
    countArray: List[DishOrder]


class Order(OrderBase):
    shopImg: str
    shopName: str
    orderDesc: str
    orderComment: bool


class CommentBase(BaseModel):
    order_id: int
    user_text: str
    user_score: int
    user_time: datetime


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    store_text: Optional[str] = None
    store_time: Optional[datetime] = None

    class Config:
        orm_mode = True


######


class SimpleReply(BaseModel):
    msg: str


class ShopDict(SimpleReply):
    shoplist: List[Dict]


class FlavorList(SimpleReply):
    foods: List[Dict]


class DishDict(SimpleReply):
    goods: List[FlavorList]


class DishItem(BaseModel):
    order_id: int
    store_id: int
    orderPrice: float
    orderShop: str
    orderImg: Optional[str] = None
    orderDesc: str
    orderComment: bool


class OrderDict(SimpleReply):
    data: List[DishItem]


class CommentDict(SimpleReply):
    data: Comment
