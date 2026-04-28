"""
seed_data.py - Populates the database with 30 sample warehouse products.

Run directly: python seed_data.py
Stock levels are varied: some full, some medium, some critically low.
"""

from datetime import date
from app import create_app
from models import db, Product


PRODUCTS: list[dict] = [
    # ── Electronics ──────────────────────────────────────────────────────────
    {
        "sku": "ELEC-001",
        "category": "Electronics",
        "name": "USB-C Charging Cable 1m",
        "current_stock": 320,
        "max_stock": 400,
        "reorder_quantity": 200,
        "last_restock_date": date(2026, 3, 10),
    },
    {
        "sku": "ELEC-002",
        "category": "Electronics",
        "name": "Wireless Keyboard",
        "current_stock": 12,
        "max_stock": 100,
        "reorder_quantity": 50,
        "last_restock_date": date(2026, 1, 22),
    },
    {
        "sku": "ELEC-003",
        "category": "Electronics",
        "name": "Wireless Mouse",
        "current_stock": 8,
        "max_stock": 100,
        "reorder_quantity": 50,
        "last_restock_date": date(2026, 1, 22),
    },
    {
        "sku": "ELEC-004",
        "category": "Electronics",
        "name": '27" Monitor',
        "current_stock": 45,
        "max_stock": 60,
        "reorder_quantity": 20,
        "last_restock_date": date(2026, 2, 14),
    },
    {
        "sku": "ELEC-005",
        "category": "Electronics",
        "name": "HDMI Cable 2m",
        "current_stock": 5,
        "max_stock": 300,
        "reorder_quantity": 150,
        "last_restock_date": date(2025, 11, 5),
    },
    {
        "sku": "ELEC-006",
        "category": "Electronics",
        "name": "USB Hub 4-Port",
        "current_stock": 60,
        "max_stock": 80,
        "reorder_quantity": 40,
        "last_restock_date": date(2026, 3, 1),
    },
    # ── Office Supplies ───────────────────────────────────────────────────────
    {
        "sku": "OFFC-001",
        "category": "Office Supplies",
        "name": "A4 Copy Paper (ream)",
        "current_stock": 900,
        "max_stock": 1000,
        "reorder_quantity": 500,
        "last_restock_date": date(2026, 4, 1),
    },
    {
        "sku": "OFFC-002",
        "category": "Office Supplies",
        "name": "Ballpoint Pens (box of 12)",
        "current_stock": 30,
        "max_stock": 200,
        "reorder_quantity": 100,
        "last_restock_date": date(2026, 1, 15),
    },
    {
        "sku": "OFFC-003",
        "category": "Office Supplies",
        "name": "Sticky Notes 3x3",
        "current_stock": 140,
        "max_stock": 150,
        "reorder_quantity": 75,
        "last_restock_date": date(2026, 3, 20),
    },
    {
        "sku": "OFFC-004",
        "category": "Office Supplies",
        "name": "Stapler",
        "current_stock": 4,
        "max_stock": 50,
        "reorder_quantity": 25,
        "last_restock_date": date(2025, 10, 12),
    },
    {
        "sku": "OFFC-005",
        "category": "Office Supplies",
        "name": "Staples (box of 5000)",
        "current_stock": 18,
        "max_stock": 100,
        "reorder_quantity": 50,
        "last_restock_date": date(2025, 12, 3),
    },
    {
        "sku": "OFFC-006",
        "category": "Office Supplies",
        "name": "Manila File Folders (pack of 25)",
        "current_stock": 200,
        "max_stock": 200,
        "reorder_quantity": 100,
        "last_restock_date": date(2026, 4, 10),
    },
    {
        "sku": "OFFC-007",
        "category": "Office Supplies",
        "name": "Whiteboard Markers (set of 4)",
        "current_stock": 10,
        "max_stock": 80,
        "reorder_quantity": 40,
        "last_restock_date": date(2025, 11, 28),
    },
    # ── Furniture ─────────────────────────────────────────────────────────────
    {
        "sku": "FURN-001",
        "category": "Furniture",
        "name": "Ergonomic Office Chair",
        "current_stock": 15,
        "max_stock": 40,
        "reorder_quantity": 10,
        "last_restock_date": date(2026, 2, 1),
    },
    {
        "sku": "FURN-002",
        "category": "Furniture",
        "name": "Standing Desk (adjustable)",
        "current_stock": 3,
        "max_stock": 20,
        "reorder_quantity": 5,
        "last_restock_date": date(2025, 12, 15),
    },
    {
        "sku": "FURN-003",
        "category": "Furniture",
        "name": "4-Drawer Filing Cabinet",
        "current_stock": 18,
        "max_stock": 20,
        "reorder_quantity": 5,
        "last_restock_date": date(2026, 3, 5),
    },
    {
        "sku": "FURN-004",
        "category": "Furniture",
        "name": "Bookshelf 5-Tier",
        "current_stock": 2,
        "max_stock": 15,
        "reorder_quantity": 5,
        "last_restock_date": date(2025, 9, 20),
    },
    {
        "sku": "FURN-005",
        "category": "Furniture",
        "name": "Folding Conference Table",
        "current_stock": 6,
        "max_stock": 10,
        "reorder_quantity": 3,
        "last_restock_date": date(2026, 1, 8),
    },
    {
        "sku": "FURN-006",
        "category": "Furniture",
        "name": "Visitor Chair",
        "current_stock": 24,
        "max_stock": 30,
        "reorder_quantity": 10,
        "last_restock_date": date(2026, 2, 18),
    },
    # ── Cleaning ──────────────────────────────────────────────────────────────
    {
        "sku": "CLEN-001",
        "category": "Cleaning",
        "name": "All-Purpose Cleaner (5L)",
        "current_stock": 8,
        "max_stock": 60,
        "reorder_quantity": 30,
        "last_restock_date": date(2025, 12, 28),
    },
    {
        "sku": "CLEN-002",
        "category": "Cleaning",
        "name": "Paper Towels (case of 12)",
        "current_stock": 55,
        "max_stock": 60,
        "reorder_quantity": 30,
        "last_restock_date": date(2026, 4, 5),
    },
    {
        "sku": "CLEN-003",
        "category": "Cleaning",
        "name": "Trash Bags 55L (box of 50)",
        "current_stock": 40,
        "max_stock": 80,
        "reorder_quantity": 40,
        "last_restock_date": date(2026, 3, 12),
    },
    {
        "sku": "CLEN-004",
        "category": "Cleaning",
        "name": "Hand Soap Refill (2L)",
        "current_stock": 6,
        "max_stock": 50,
        "reorder_quantity": 25,
        "last_restock_date": date(2025, 11, 10),
    },
    {
        "sku": "CLEN-005",
        "category": "Cleaning",
        "name": "Disinfectant Wipes (canister)",
        "current_stock": 90,
        "max_stock": 100,
        "reorder_quantity": 50,
        "last_restock_date": date(2026, 4, 8),
    },
    {
        "sku": "CLEN-006",
        "category": "Cleaning",
        "name": "Mop & Bucket Set",
        "current_stock": 5,
        "max_stock": 10,
        "reorder_quantity": 3,
        "last_restock_date": date(2026, 1, 30),
    },
    # ── Packaging ─────────────────────────────────────────────────────────────
    {
        "sku": "PACK-001",
        "category": "Packaging",
        "name": "Cardboard Boxes Small (pack of 20)",
        "current_stock": 7,
        "max_stock": 200,
        "reorder_quantity": 100,
        "last_restock_date": date(2025, 10, 5),
    },
    {
        "sku": "PACK-002",
        "category": "Packaging",
        "name": "Cardboard Boxes Large (pack of 10)",
        "current_stock": 150,
        "max_stock": 150,
        "reorder_quantity": 75,
        "last_restock_date": date(2026, 4, 2),
    },
    {
        "sku": "PACK-003",
        "category": "Packaging",
        "name": "Bubble Wrap Roll 50m",
        "current_stock": 12,
        "max_stock": 30,
        "reorder_quantity": 15,
        "last_restock_date": date(2026, 2, 22),
    },
    {
        "sku": "PACK-004",
        "category": "Packaging",
        "name": "Packing Tape 48mm (case of 36)",
        "current_stock": 3,
        "max_stock": 36,
        "reorder_quantity": 18,
        "last_restock_date": date(2025, 12, 1),
    },
    {
        "sku": "PACK-005",
        "category": "Packaging",
        "name": "Shipping Labels A4 (pack of 100)",
        "current_stock": 250,
        "max_stock": 300,
        "reorder_quantity": 150,
        "last_restock_date": date(2026, 3, 28),
    },
]


def seed(clear_existing: bool = False) -> None:
    """Seed the database with sample product data.

    Args:
        clear_existing: If True, delete all existing products before inserting.
    """
    app = create_app()
    with app.app_context():
        if clear_existing:
            Product.query.delete()
            db.session.commit()
            print("Cleared existing products.")

        inserted = 0
        skipped = 0
        for data in PRODUCTS:
            if Product.query.filter_by(sku=data["sku"]).first():
                skipped += 1
                continue
            db.session.add(Product(**data))
            inserted += 1

        db.session.commit()
        print(f"Seeding complete: {inserted} inserted, {skipped} skipped (already exist).")


if __name__ == "__main__":
    seed()
