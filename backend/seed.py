from sqlalchemy.orm import Session
from models import Restaurant, Category, MenuItem


def seed_database(db: Session):
    if db.query(Restaurant).count() > 0:
        return  # Already seeded

    # ── Restaurant ──
    r = Restaurant(
        name="Spice Garden",
        slug="spice-garden",
        description="Authentic Indian cuisine crafted with love and the finest spices.",
        address="12 MG Road, Bengaluru, Karnataka 560001",
        whatsapp_number="919660920036", 
        logo_url="",
        cover_url="",
        currency="₹",
    )
    db.add(r)
    db.flush()

    # ── Categories & Items ──
    menu = [
        {
            "name": "Starters", "emoji": "🔥", "sort_order": 1,
            "items": [
                {"name": "Paneer Tikka", "price": 249, "is_veg": True,  "is_bestseller": True,  "spice_level": 2,
                 "description": "Soft cottage cheese cubes marinated in yogurt and spices, grilled to perfection.",
                 "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400"},
                {"name": "Chicken 65",   "price": 299, "is_veg": False, "is_bestseller": True,  "spice_level": 3,
                 "description": "Crispy deep-fried chicken with a tangy, spicy south Indian marinade.",
                 "image_url": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=400"},
                {"name": "Veg Seekh Kebab","price":199,"is_veg": True,  "is_bestseller": False, "spice_level": 1,
                 "description": "Minced vegetables and paneer blended with herbs, skewered and flame-grilled.",
                 "image_url": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400"},
                {"name": "Fish Amritsari","price":349,"is_veg": False, "is_bestseller": False, "spice_level": 2,
                 "description": "Golden fried fish fillets coated in a classic Amritsari spice batter.",
                 "image_url": "https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=400"},
            ]
        },
        {
            "name": "Biryani", "emoji": "🍛", "sort_order": 2,
            "items": [
                {"name": "Hyderabadi Dum Biryani", "price": 349, "is_veg": False,"is_bestseller": True, "spice_level": 2,
                 "description": "Slow-cooked basmati rice layered with tender mutton in the authentic dum style.",
                 "image_url": "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=400"},
                {"name": "Veg Dum Biryani",         "price": 249, "is_veg": True, "is_bestseller": False,"spice_level": 1,
                 "description": "Fragrant basmati layered with seasonal vegetables and whole spices.",
                 "image_url": "https://images.unsplash.com/photo-1596560548464-f010549b84d7?w=400"},
                {"name": "Chicken Biryani",          "price": 319, "is_veg": False,"is_bestseller": True, "spice_level": 2,
                 "description": "Juicy chicken pieces slow-cooked with basmati rice and aromatic spices.",
                 "image_url": "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=400"},
                {"name": "Prawn Biryani",            "price": 399, "is_veg": False,"is_bestseller": False,"spice_level": 3,
                 "description": "Succulent prawns tossed in coastal masala, layered with saffron rice.",
                 "image_url": "https://images.unsplash.com/photo-1590502160462-58b41354f588?w=400"},
            ]
        },
        {
            "name": "Curries", "emoji": "🥘", "sort_order": 3,
            "items": [
                {"name": "Butter Chicken",   "price": 329, "is_veg": False,"is_bestseller": True, "spice_level": 1,
                 "description": "Tender chicken in a rich, creamy tomato-based sauce with fenugreek.",
                 "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=400"},
                {"name": "Dal Makhani",      "price": 229, "is_veg": True, "is_bestseller": True, "spice_level": 1,
                 "description": "Slow-simmered black lentils in a buttery, velvety tomato gravy.",
                 "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400"},
                {"name": "Palak Paneer",     "price": 259, "is_veg": True, "is_bestseller": False,"spice_level": 1,
                 "description": "Cottage cheese cubes in a smooth, seasoned spinach gravy.",
                 "image_url": "https://images.unsplash.com/photo-1589647363585-f4a7d3877b10?w=400"},
                {"name": "Lamb Rogan Josh",  "price": 379, "is_veg": False,"is_bestseller": False,"spice_level": 3,
                 "description": "Kashmiri-style slow-braised lamb in a bold, aromatic red gravy.",
                 "image_url": "https://images.unsplash.com/photo-1604152135912-04a022e23696?w=400"},
            ]
        },
        {
            "name": "Breads", "emoji": "🫓", "sort_order": 4,
            "items": [
                {"name": "Garlic Naan",    "price": 79,  "is_veg": True,  "is_bestseller": True,  "spice_level": 0,
                 "description": "Fluffy tandoor bread brushed with garlic butter and fresh coriander.",
                 "image_url": "https://images.unsplash.com/photo-1584736286279-5d85e31f2ea4?w=400"},
                {"name": "Laccha Paratha", "price": 69,  "is_veg": True,  "is_bestseller": False, "spice_level": 0,
                 "description": "Flaky, layered whole wheat flatbread from the tawa.",
                 "image_url": "https://images.unsplash.com/photo-1607532941433-304659e8198a?w=400"},
                {"name": "Stuffed Kulcha", "price": 99,  "is_veg": True,  "is_bestseller": False, "spice_level": 1,
                 "description": "Soft bread stuffed with spiced potato and onion, baked in tandoor.",
                 "image_url": "https://images.unsplash.com/photo-1576157374051-4ee2cdc4a8be?w=400"},
            ]
        },
        {
            "name": "Desserts", "emoji": "🍮", "sort_order": 5,
            "items": [
                {"name": "Gulab Jamun",   "price": 99,  "is_veg": True, "is_bestseller": True,  "spice_level": 0,
                 "description": "Soft milk-solid dumplings soaked in rose-cardamom sugar syrup.",
                 "image_url": "https://images.unsplash.com/photo-1601303516534-bf5d69b0d96d?w=400"},
                {"name": "Rasmalai",      "price": 129, "is_veg": True, "is_bestseller": False, "spice_level": 0,
                 "description": "Spongy paneer discs soaked in chilled saffron-flavoured milk.",
                 "image_url": "https://images.unsplash.com/photo-1631452180539-96aca7d48617?w=400"},
                {"name": "Kulfi Falooda", "price": 149, "is_veg": True, "is_bestseller": True,  "spice_level": 0,
                 "description": "Traditional ice cream with vermicelli, basil seeds and rose syrup.",
                 "image_url": "https://images.unsplash.com/photo-1567337710282-00832b415979?w=400"},
            ]
        },
        {
            "name": "Drinks", "emoji": "🥤", "sort_order": 6,
            "items": [
                {"name": "Mango Lassi",       "price": 99,  "is_veg": True, "is_bestseller": True,  "spice_level": 0,
                 "description": "Thick, creamy yogurt blended with sweet Alphonso mango pulp.",
                 "image_url": "https://images.unsplash.com/photo-1571167530149-c1105da4c2f4?w=400"},
                {"name": "Masala Chaas",      "price": 69,  "is_veg": True, "is_bestseller": False, "spice_level": 1,
                 "description": "Spiced buttermilk with cumin, ginger and fresh mint.",
                 "image_url": "https://images.unsplash.com/photo-1638437447450-6e0f58dc8db5?w=400"},
                {"name": "Virgin Mojito",     "price": 119, "is_veg": True, "is_bestseller": False, "spice_level": 0,
                 "description": "Fresh lime, mint and soda over crushed ice.",
                 "image_url": "https://images.unsplash.com/photo-1574090945491-e13cb157bdf6?w=400"},
            ]
        },
    ]

    for cat_data in menu:
        items = cat_data.pop("items")
        cat = Category(restaurant_id=r.id, **cat_data)
        db.add(cat)
        db.flush()
        for i, it in enumerate(items):
            db.add(MenuItem(category_id=cat.id, sort_order=i, **it))

    db.commit()
    print("✅ Database seeded with Spice Garden restaurant data.")