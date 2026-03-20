from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    ForeignKey, Text, DateTime, func,
)
from sqlalchemy.orm import relationship
from database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(120), nullable=False)
    slug          = Column(String(80), unique=True, nullable=False, index=True)
    description   = Column(Text, default="")
    address       = Column(String(255), default="")
    whatsapp_number = Column(String(20), nullable=False)   # e.g. "919876543210"
    logo_url      = Column(String(500), default="")
    cover_url     = Column(String(500), default="")
    currency      = Column(String(5), default="₹")
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())

    categories = relationship("Category", back_populates="restaurant",
                              cascade="all, delete-orphan")
    orders     = relationship("Order", back_populates="restaurant")


class Category(Base):
    __tablename__ = "categories"

    id            = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name          = Column(String(80), nullable=False)
    description   = Column(String(255), default="")
    emoji         = Column(String(10), default="🍽️")
    sort_order    = Column(Integer, default=0)
    is_active     = Column(Boolean, default=True)

    restaurant = relationship("Restaurant", back_populates="categories")
    items      = relationship("MenuItem", back_populates="category",
                              cascade="all, delete-orphan")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id          = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name        = Column(String(120), nullable=False)
    description = Column(Text, default="")
    price       = Column(Float, nullable=False)
    image_url   = Column(String(500), default="")
    is_veg      = Column(Boolean, default=True)
    is_available= Column(Boolean, default=True)
    is_bestseller = Column(Boolean, default=False)
    spice_level = Column(Integer, default=0)   # 0-3
    sort_order  = Column(Integer, default=0)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    category    = relationship("Category", back_populates="items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class Order(Base):
    __tablename__ = "orders"

    id              = Column(Integer, primary_key=True, index=True)
    restaurant_id   = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    customer_name   = Column(String(120), default="")
    customer_phone  = Column(String(20), default="")
    notes           = Column(Text, default="")
    total_amount    = Column(Float, default=0.0)
    status          = Column(String(30), default="pending")
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    restaurant  = relationship("Restaurant", back_populates="orders")
    items       = relationship("OrderItem", back_populates="order",
                               cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id           = Column(Integer, primary_key=True, index=True)
    order_id     = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity     = Column(Integer, nullable=False)
    unit_price   = Column(Float, nullable=False)
    subtotal     = Column(Float, nullable=False)

    order     = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")