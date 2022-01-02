from sqlalchemy.orm import Session

from . import models, schemas


def get_shop(db: Session, shop_id: int):
    print("here")
    return db.query(models.Shop).filter(models.Shop.id == shop_id).first()


def get_shop_by_phone(db: Session, phone: str):
    return db.query(models.Shop).filter(models.Shop.phone == phone).first()


def get_shops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shop).offset(skip).limit(limit).all()


def create_shop(db: Session, shop: schemas.ShopCreate):
    fake_hashed_password = shop.password + "notreallyhashed"
    db_shop = models.Shop(phone=shop.phone, password=fake_hashed_password)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def get_dishs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dish).offset(skip).limit(limit).all()


def create_shop_dish(db: Session, dish: schemas.DishCreate, shop_id: int):
    db_dish = models.Dish(**dish.dict(), store_id=shop_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
