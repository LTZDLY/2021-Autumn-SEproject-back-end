import datetime
from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def get_shop(db: Session, shop_id: int):
    return db.query(models.Shop).filter(models.Shop.id == shop_id).first()


def get_shop_by_phone(db: Session, phone: str):
    return db.query(models.Shop).filter(models.Shop.phone == phone).first()


def get_shop_by_id(db: Session, id: int):
    return db.query(models.Shop).filter(models.Shop.id == id).first()


def get_dish_by_id(db: Session, id: int):
    return db.query(models.Dish).filter(models.Dish.id == id).first()


def get_shops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shop).offset(skip).limit(limit).all()


def get_evaluates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order_by_id(db: Session, id: int):
    return db.query(models.Order).filter(models.Order.id == id).first()

def get_orders_by_store_id(db: Session, store_id: int):
    return db.query(models.Order).filter(models.Order.store_id == store_id).all()


def get_order_dish(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order_Dish).offset(skip).limit(limit).all()


def get_order_status(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order_Status).offset(skip).limit(limit).all()


def create_user(db: Session, openid: str):
    db_user = models.User(openid=openid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_order(db: Session, user_id: int, order: schemas.OrderCreate):
    db_order = models.Order(
        store_id=order.store_id, user_id=user_id, price=order.totalPrice
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order.id


def add_order_dish(db: Session, order_id: int, dishes: List[schemas.DishOrder]):
    for i in dishes:
        db_order_dish = models.Order_Dish(order_id=order_id, dish_id=i.id, num=i.num)
        db.add(db_order_dish)
        db.commit()


def create_order_status(db: Session, order_id: int):
    db_order_status = models.Order_Status(
        order_id=order_id, submit_time=datetime.datetime.now()
    )
    db.add(db_order_status)
    db.commit()


def get_user_by_openid(db: Session, openid: str):
    return db.query(models.User).filter(models.User.open_id == openid).first()


def get_comment_by_order_id(db: Session, order_id: int):
    return db.query(models.Comment).filter(models.Comment.order_id == order_id).first()


def get_comment_by_store_id(db: Session, store_id: int):
    return (
        db.query(models.Shop)
        .join(models.Comment)
        .filter(models.Shop.id == store_id)
        .all()
    )


def create_shop(db: Session, shop: schemas.ShopCreate):
    # fake_hashed_password = shop.password + "notreallyhashed"
    db_shop = models.Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_dishs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dish).offset(skip).limit(limit).all()


def get_dishs_by_store_id(db: Session, store_id: str):
    return db.query(models.Dish).filter(models.Dish.store_id == store_id).all()


def create_dish(db: Session, dish: schemas.DishCreate, shop_id: int):
    db_dish = models.Dish(**dish.dict(), store_id=shop_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def get_all_order(db: Session, user_id: int):
    results = (
        db.query(
            models.Order.id,
            models.Order.store_id,
            models.Order.price,
            models.Shop.name,
            models.Shop.img,
        )
        .filter(models.Order.user_id == user_id)
        .join(models.Shop)
        .all()
    )
    ans = []
    for i in results:
        sql = """
            SELECT `order-dish`.num, `dish`.describe, `order_status`.comment
            FROM `order-dish`
            INNER JOIN `dish` ON `dish`.id = `order-dish`.dish_id
            INNER JOIN `order_status` ON `order_status`.order_id = `order-dish`.order_id
            WHERE `order-dish`.order_id = {}
        """.format(
            i[0]
        )
        res = db.execute(sql).fetchall()
        s = ""
        for j in res:
            s += f"{j[1]}×{j[0]}, "
        temp = {
            "order_id": i[0],
            "store_id": i[1],
            "orderPrice": i[2],
            "orderShop": i[3],
            "orderImg": i[4],
            "orderDesc": s,
            "orderComment": res[0][2],
        }
        ans.append(temp)
    return ans

def change_shop_by_id(db: Session, id: str, shop: schemas.ShopChange):
    db.query(models.Shop).filter(models.Shop.id == id).update(shop.dict())
    db.commit()
    return db.query(models.Shop).filter(models.Shop.id == id).first()