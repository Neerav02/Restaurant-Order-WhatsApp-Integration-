"""
Restaurant Ordering System - FastAPI Backend
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, engine, Base
from models import Restaurant, Category, MenuItem, Order, OrderItem
from schemas import (
    RestaurantCreate, RestaurantRead,
    CategoryCreate, CategoryRead,
    MenuItemCreate, MenuItemRead,
    OrderCreate, OrderRead,
)
from seed import seed_database

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant Ordering API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    db = next(get_db())
    seed_database(db)


# ─── Restaurants ──────────────────────────────────────────────────────────────

@app.get("/restaurants", response_model=List[RestaurantRead])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).filter(Restaurant.is_active == True).all()


@app.get("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return r


@app.post("/restaurants", response_model=RestaurantRead)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    r = Restaurant(**data.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@app.patch("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(restaurant_id: int, data: RestaurantCreate, db: Session = Depends(get_db)):
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r


# ─── Categories ───────────────────────────────────────────────────────────────

@app.get("/restaurants/{restaurant_id}/categories", response_model=List[CategoryRead])
def list_categories(restaurant_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Category)
        .filter(Category.restaurant_id == restaurant_id, Category.is_active == True)
        .order_by(Category.sort_order)
        .all()
    )


@app.post("/restaurants/{restaurant_id}/categories", response_model=CategoryRead)
def create_category(restaurant_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    cat = Category(restaurant_id=restaurant_id, **data.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


# ─── Menu Items ───────────────────────────────────────────────────────────────

@app.get("/restaurants/{restaurant_id}/menu", response_model=List[MenuItemRead])
def get_full_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MenuItem)
        .join(Category)
        .filter(Category.restaurant_id == restaurant_id, MenuItem.is_available == True)
        .order_by(Category.sort_order, MenuItem.sort_order)
        .all()
    )


@app.get("/categories/{category_id}/items", response_model=List[MenuItemRead])
def list_items(category_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MenuItem)
        .filter(MenuItem.category_id == category_id, MenuItem.is_available == True)
        .order_by(MenuItem.sort_order)
        .all()
    )


@app.post("/categories/{category_id}/items", response_model=MenuItemRead)
def create_item(category_id: int, data: MenuItemCreate, db: Session = Depends(get_db)):
    item = MenuItem(category_id=category_id, **data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.patch("/items/{item_id}", response_model=MenuItemRead)
def update_item(item_id: int, data: MenuItemCreate, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@app.patch("/items/{item_id}/price")
def update_price(item_id: int, price: float, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.price = price
    db.commit()
    return {"id": item_id, "new_price": price}


# ─── Orders ───────────────────────────────────────────────────────────────────

@app.post("/orders", response_model=OrderRead)
def place_order(data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        restaurant_id=data.restaurant_id,
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        notes=data.notes,
        total_amount=0,
    )
    db.add(order)
    db.flush()

    total = 0.0
    for oi in data.items:
        item = db.query(MenuItem).filter(MenuItem.id == oi.menu_item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item {oi.menu_item_id} not found")
        subtotal = item.price * oi.quantity
        total += subtotal
        db.add(OrderItem(
            order_id=order.id,
            menu_item_id=item.id,
            quantity=oi.quantity,
            unit_price=item.price,
            subtotal=subtotal,
        ))

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order


@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)