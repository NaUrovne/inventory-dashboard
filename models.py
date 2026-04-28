"""
models.py - Database setup and Product model for the warehouse inventory tool.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()


class Product(db.Model):
    """Represents a single inventory item tracked in the warehouse."""

    __tablename__ = "products"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku: str = db.Column(db.String(50), unique=True, nullable=False)
    category: str = db.Column(db.String(100), nullable=False)
    name: str = db.Column(db.String(200), nullable=False)
    current_stock: int = db.Column(db.Integer, nullable=False, default=0)
    max_stock: int = db.Column(db.Integer, nullable=False)
    reorder_quantity: int = db.Column(db.Integer, nullable=False)
    last_restock_date: date = db.Column(db.Date, nullable=True)

    def is_low_stock(self) -> bool:
        """Return True if current stock is at or below 20% of max capacity."""
        return self.current_stock <= (self.max_stock * 0.20)

    def stock_percentage(self) -> float:
        """Return current stock as a percentage of max stock."""
        if self.max_stock == 0:
            return 0.0
        return round((self.current_stock / self.max_stock) * 100, 1)

    def __repr__(self) -> str:
        return f"<Product sku={self.sku!r} name={self.name!r} stock={self.current_stock}/{self.max_stock}>"


class ReorderListItem(db.Model):
    """A single entry on the purchasing team's reorder list."""

    __tablename__ = "reorder_list_items"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    quantity: int = db.Column(db.Integer, nullable=False)
    added_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product = db.relationship("Product", backref="reorder_items", lazy="joined")

    __table_args__ = (
        db.CheckConstraint("quantity > 0", name="quantity_positive"),
    )

    def __repr__(self) -> str:
        return f"<ReorderListItem product_id={self.product_id} quantity={self.quantity}>"
