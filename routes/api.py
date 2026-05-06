"""
routes/api.py - JSON API endpoints consumed by the Order API service.
"""

from flask import Blueprint, jsonify, request
from models import db, Product

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _product_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "sku": p.sku,
        "category": p.category,
        "name": p.name,
        "current_stock": p.current_stock,
        "max_stock": p.max_stock,
        "reorder_quantity": p.reorder_quantity,
        "last_restock_date": p.last_restock_date.isoformat() if p.last_restock_date else None,
        "stock_percentage": p.stock_percentage(),
    }


@api_bp.get("/products")
def get_products():
    """Return all products, optionally filtered by category."""
    category = request.args.get("category")
    query = Product.query.order_by(Product.category, Product.name)
    if category:
        query = query.filter(Product.category == category)
    products = query.all()
    return jsonify({"count": len(products), "products": [_product_dict(p) for p in products]})


@api_bp.get("/products/<sku>")
def get_product(sku: str):
    """Return a single product by SKU."""
    product = Product.query.filter_by(sku=sku).first()
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(_product_dict(product))


@api_bp.patch("/products/<sku>/stock")
def update_stock(sku: str):
    """Adjust current_stock by a signed integer amount."""
    product = Product.query.filter_by(sku=sku).first()
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json(silent=True) or {}
    adjustment = data.get("adjustment")
    reason = data.get("reason")

    if not isinstance(adjustment, int):
        return jsonify({"error": "'adjustment' must be an integer"}), 400
    if not isinstance(reason, str) or not reason.strip():
        return jsonify({"error": "'reason' must be a non-empty string"}), 400

    new_stock = product.current_stock + adjustment
    if new_stock < 0:
        return jsonify({
            "error": "Adjustment would bring stock below 0",
            "current_stock": product.current_stock,
            "adjustment": adjustment,
        }), 422
    if new_stock > product.max_stock:
        return jsonify({
            "error": "Adjustment would exceed max_stock",
            "current_stock": product.current_stock,
            "max_stock": product.max_stock,
            "adjustment": adjustment,
        }), 422

    product.current_stock = new_stock
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to update stock"}), 500

    return jsonify(_product_dict(product))
