from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shops/", response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_db)):
    db_shop = crud.get_shop_by_email(db, email=shop.email)
    if db_shop:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_shop(db=db, shop=shop)


@app.get("/shops/", response_model=List[schemas.Shop])
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shops = crud.get_shops(db, skip=skip, limit=limit)
    return shops


@app.get("/shops{shop_id}", response_model=schemas.Shop)
def read_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@app.post("/shops{shop_id}/dishs/", response_model=schemas.Dish)
def create_dish_for_shop(
    shop_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)
):
    return crud.create_shop_dish(db=db, dish=dish, shop_id=shop_id)


@app.get("/dishs/", response_model=List[schemas.Dish])
def read_dishs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishs = crud.get_dishs(db, skip=skip, limit=limit)
    return dishs
