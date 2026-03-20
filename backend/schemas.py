from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ─── Restaurant ───────────────────────────────────────────────────────────────

class RestaurantCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = ""
    address: Optional[str] = ""
    whatsapp_number: str
    logo_url: Optional[str] = ""
    cover_url: Optional[str] = ""
    currency: Optional[str] = "₹"
    is_active: Optional[bool] = True


class RestaurantRead(RestaurantCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─── Category ─────────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    emoji: Optional[str] = "🍽️"
    sort_order: Optional[int] = 0
    is_active: Optional[bool] = True


class CategoryRead(CategoryCreate):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True


# ─── Menu Item ────────────────────────────────────────────────────────────────

class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    image_url: Optional[str] = ""
    is_veg: Optional[bool] = True
    is_available: Optional[bool] = True
    is_bestseller: Optional[bool] = False
    spice_level: Optional[int] = 0
    sort_order: Optional[int] = 0


class MenuItemRead(MenuItemCreate):
    id: int
    category_id: int

    class Config:
        from_attributes = True


# ─── Order ────────────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    restaurant_id: int
    customer_name: Optional[str] = ""
    customer_phone: Optional[str] = ""
    notes: Optional[str] = ""
    items: List[OrderItemCreate]


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderRead(BaseModel):
    id: int
    restaurant_id: int
    customer_name: str
    customer_phone: str
    notes: str
    total_amount: float
    status: str
    created_at: Optional[datetime]
    items: List[OrderItemRead]

    class Config:
        from_attributes = True