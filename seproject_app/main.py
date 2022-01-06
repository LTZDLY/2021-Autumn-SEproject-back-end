from typing import List, Optional

import requests
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, responses
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .data.data import address, testopenid
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


@app.get("/getopenid")
def fun(response: Response):
    response.set_cookie(key="openid", value=testopenid)
    return


@app.get("/getshopid")
def fun(shopid: int, response: Response):
    response.set_cookie(key="shopid", value=shopid)
    return


"""
@app.post("/shops/", response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_db)):
    db_shop = crud.get_shop_by_phone(db, phone=shop.phone)
    if db_shop:
        raise HTTPException(status_code=400, detail="Phone already registered")
    return crud.create_shop(db=db, shop=shop)


@app.get("/shops", response_model=List[schemas.Shop])
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shops = crud.get_shops(db, skip=skip, limit=limit)
    return shops


@app.get("/orders/")
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/order_dish/")
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_order_dish(db, skip=skip, limit=limit)
    return orders


@app.get("/order_status/")
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_order_status(db, skip=skip, limit=limit)
    return orders


@app.get("/evlauates/")
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evaluates = crud.get_evaluates(db, skip=skip, limit=limit)
    return evaluates


@app.get("/shops/{shop_id}", response_model=schemas.Shop)
def read_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@app.post("/shops/{shop_id}/dishs/", response_model=schemas.Dish)
def create_dish_for_shop(
    shop_id: int, dish: schemas.DishCreate, db: Session = Depends(get_db)
):
    return crud.create_shop_dish(db=db, dish=dish, shop_id=shop_id)


@app.get("/dishs/", response_model=List[schemas.Dish])
def read_dishs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dishs = crud.get_dishs(db, skip=skip, limit=limit)
    return dishs
"""


@app.get("/api/seproject/get_openid", response_model=schemas.User)
# 顾客wx登录
def getid(code: str, db: Session = Depends(get_db)):
    url = "https://api.weixin.qq.com/sns/jscode2session"
    appid = "wxb5602a69aaaf3ccf"
    secret = "e03f269d14a9a330c25839d014c2f26a"
    params = {
        "appid": appid,
        "secret": secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }

    data = requests.get(url, params=params).json()
    # print(data)
    if "openid" not in data:
        resp = responses.JSONResponse(content=data)
        return resp

    openid = data["openid"]
    db_user = crud.get_user_by_openid(db, openid)
    if not db_user:
        db_user = crud.create_user(db=db, user=openid)

    resp = responses.JSONResponse(content={"id": db_user.id})
    resp.set_cookie(key="openid", value=id)
    return resp


@app.get("/api/seproject/getstoreinfo", response_model=schemas.ShopDict)
# 顾客获取店铺信息
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shops = crud.get_shops(db, skip=skip, limit=limit)
    l = []
    for i in shops:
        d = {
            "id": i.id,
            "shopName": i.name,
            "shopDesc": i.describe,
            "shopText": "距离{}m".format(i.distance),
            "shopImg": None,
        }
        if i.img is not None:
            d["shopImg"] = f"{address}{i.img}"
        l.append(d)
        pass
    data = schemas.ShopDict(msg="ok", shoplist=l)
    return data


@app.get("/api/seproject/getdishinfo", response_model=schemas.DishDict)
# 顾客获取菜品信息
def get_dish_info(store_id: int, db: Session = Depends(get_db)):
    if not store_id:
        raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        dishs = crud.get_dishs_by_store_id(db, store_id)
        data = schemas.DishDict(msg="ok", goods=[])
        h = {}
        foodlist = []
        for inx, i in enumerate(dishs):
            if not i.flavor in h:
                h[i.flavor] = [inx]
            else:
                h[i.flavor].append(inx)
            d = {
                "name": i.describe,
                "price": i.price,
                "id": i.id,
                "description": i.description,
                "icon": None,
                "Count": 0,
            }
            if i.icon is not None:
                d["icon"] = f"{address}{i.icon}"
            foodlist.append(d)
        temp = []
        for i in h:
            d = schemas.FlavorList(name=i, foods=[])
            for j in h[i]:
                d.foods.append(foodlist[j])
            temp.append(d)
        data.goods = temp
    return data


@app.post("/api/seproject/createOrder")
# 顾客创建订单
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    openid: Optional[str] = Cookie(None),
):
    if not openid:
        raise HTTPException(status_code=401, detail="please login first")

    user = crud.get_user_by_openid(db, openid)

    # 错误检查
    price = 0.0
    store = crud.get_shop_by_id(db, order.store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    for i in order.countArray:
        dish = crud.get_dish_by_id(db, i.id)
        if dish is None:
            raise HTTPException(status_code=404, detail="Dish not found")
        if dish.store_id != store.id:
            raise HTTPException(status_code=400, detail="Not a dish in this shop")
        price += dish.price * i.num

    order.totalPrice = round(price, 2)
    # 订单表内加订单
    order_id = crud.create_order(db, user.id, order)
    # 订单-菜品表加数据
    crud.add_order_dish(db, order_id, order.countArray)
    # 订单状态表加数据
    crud.create_order_status(db, order_id)
    data = {"msg": "succeed", "order_id": order_id}
    resp = responses.JSONResponse(content=data)
    return resp


@app.get("/api/seproject/getAllOrders", response_model=schemas.OrderDict)
# 顾客获取自己的全部订单
def get_all_orders(db: Session = Depends(get_db), openid: Optional[str] = Cookie(None)):
    if not openid:
        raise HTTPException(status_code=401, detail="please login first")

    user = crud.get_user_by_openid(db, openid)
    return schemas.OrderDict(msg="succeed", data=crud.get_all_order(db, user.id))


@app.get("/api/seproject/getComment", response_model=schemas.CommentDict)
# 顾客获取评论信息
def get_comment(order_id: int, db: Session = Depends(get_db)):
    if not order_id:
        raise HTTPException(status_code=400, detail="Missing parameter")

    db_comment = crud.get_comment_by_order_id(db, order_id)
    return schemas.CommentDict(msg="succeed", data=db_comment)


# TODO 写到这里
@app.post("/api/seproject/addComment", response_model=schemas.SimpleReply)
# 顾客增加评论
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    openid: Optional[str] = Cookie(None),
):
    if not openid:
        raise HTTPException(status_code=401, detail="please login first")

    db_comment = crud.get_comment_by_order_id(db, comment.order_id)
    if db_comment:
        raise HTTPException(status_code=400, detail="Comment already exists")

    db_order = crud.get_order_by_id(db, comment.order_id)
    user = crud.get_user_by_openid(db, openid)
    if db_order is None:
        raise HTTPException(status_code=400, detail="Order not found")
    if db_order.user_id != user.id:
        raise HTTPException(status_code=400, detail="You have no permission to do this")

    crud.create_comment(db, comment)
    return schemas.SimpleReply(msg="succeed")


############################
# 以下为商家模块


@app.post("/api/seproject/shop/sign_in", response_model=schemas.Shop)
# 商家登录
def signin(shop: schemas.ShopLogin, response: Response, db: Session = Depends(get_db)):
    db_shop = crud.get_shop_by_phone(db, phone=shop.phone)
    if db_shop is None:
        raise HTTPException(status_code=400, detail="Shop not found")
    if db_shop.password != shop.password:
        raise HTTPException(status_code=400, detail="Wrong password, try again")
    response.set_cookie(key="shopid", value=db_shop.id)
    return db_shop


@app.post("/api/seproject/shop/sign_up", response_model=schemas.Shop)
# 商家注册
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_db)):
    db_shop = crud.get_shop_by_phone(db, phone=shop.phone)
    if db_shop:
        raise HTTPException(status_code=400, detail="Phone already registered")
    return crud.create_shop(db=db, shop=shop)


@app.post("/api/seproject/shop/change_info", response_model=schemas.Shop)
# 商家修改信息
def change_shop(
    shop: schemas.ShopChange,
    db: Session = Depends(get_db),
    shopid: Optional[str] = Cookie(None),
):
    if not shopid:
        raise HTTPException(status_code=401, detail="please login first")

    return crud.change_shop_by_id(db, shopid, shop)


@app.post("/api/seproject/shop/create_dish", response_model=schemas.Dish)
# 商家添加菜品
def create_dish(
    dish: schemas.DishCreate,
    db: Session = Depends(get_db),
    shopid: Optional[str] = Cookie(None),
):
    if not shopid:
        raise HTTPException(status_code=401, detail="please login first")
    return crud.create_dish(db, dish, shopid)

"""
@app.get("/api/seproject/getShopInfo")
def get_shop_info(phone: int):
    # 商家获取商店信息
    if not phone:
        data = {"msg": "Failed"}
        resp = responses.JSONResponse(content=data)
        return resp

    data_raw = mysql.get_shop_info(phone)

    data = {
        "msg": "succeed",
        "data": {
            "id": data_raw[0],
            "name": data_raw[1],
            "address": data_raw[5],
            "description": data_raw[4],
        },
    }
    resp = responses.JSONResponse(content=data)
    return resp


@app.get("/api/seproject/getShopDishInfo")
def get_shop_dish_info(phone: int):
    # 商家获取所有的菜品信息
    if not phone:
        data = {"msg": "Failed"}
        resp = responses.JSONResponse(content=data)
        return resp

    data_raw = mysql.get_shop_dish_info(phone)
    ans = []
    for i in data_raw:
        temp = {
            "id": i[0],
            "name": i[2],
            "flavor": i[3],
            "price": i[4],
            "description": i[5],
            "icon": i[6],
        }
        ans.append(temp)
    data = {"msg": "succeed", "data": ans}
    resp = responses.JSONResponse(content=data)
    return resp
    """
