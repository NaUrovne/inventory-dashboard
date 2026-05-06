"""
app.py - Flask application factory and configuration for the warehouse inventory tool.
"""

import io
import os
from datetime import date
from flask import Flask, render_template, jsonify, abort, request, send_file
from models import db, Product, ReorderListItem
from routes.api import api_bp
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def create_app(db_path: str = "inventory.db") -> Flask:
    """Create and configure the Flask application.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(base_dir, db_path)}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp)

    @app.route("/")
    def dashboard() -> str:
        """Render the inventory dashboard with all products and summary counts."""
        products = Product.query.order_by(Product.category, Product.name).all()

        counts = {"critical": 0, "low": 0, "healthy": 0}
        for p in products:
            pct = (p.current_stock / p.max_stock * 100) if p.max_stock else 0
            if pct < 15:
                counts["critical"] += 1
            elif pct < 30:
                counts["low"] += 1
            else:
                counts["healthy"] += 1

        reorder_ids = {item.product_id for item in ReorderListItem.query.all()}
        reorder_count = len(reorder_ids)
        return render_template(
            "dashboard.html",
            products=products,
            counts=counts,
            reorder_ids=reorder_ids,
            reorder_count=reorder_count,
        )

    @app.route("/reorder")
    def reorder() -> str:
        """Render the reorder list page."""
        items = ReorderListItem.query.order_by(ReorderListItem.added_at).all()
        return render_template("reorder.html", items=items)

    @app.post("/reorder/add/<int:product_id>")
    def reorder_add(product_id: int):
        """Insert a product into the reorder list using its default reorder_quantity."""
        product = db.session.get(Product, product_id)
        if product is None:
            abort(404)
        existing = ReorderListItem.query.filter_by(product_id=product_id).first()
        if existing:
            return jsonify({"status": "already_added", "count": ReorderListItem.query.count()})
        gap = product.max_stock - product.current_stock
        if gap <= 0:
            return jsonify({"status": "error", "message": "Product is fully stocked"}), 400
        item = ReorderListItem(product_id=product_id, quantity=gap)
        db.session.add(item)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({"status": "error", "message": "Failed to add item"}), 500
        return jsonify({"status": "added", "count": ReorderListItem.query.count()})

    @app.patch("/reorder/update/<int:product_id>")
    def reorder_update(product_id: int):
        """Update the quantity for an existing reorder list item."""
        item = ReorderListItem.query.filter_by(product_id=product_id).first()
        if item is None:
            abort(404)
        data = request.get_json(silent=True) or {}
        quantity = data.get("quantity")
        if not isinstance(quantity, int) or quantity < 1:
            abort(400)
        gap = item.product.max_stock - item.product.current_stock
        if gap <= 0:
            return jsonify({"status": "error", "message": "Product is fully stocked"}), 400
        item.quantity = min(quantity, gap)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({"status": "error", "message": "Failed to update item"}), 500
        return jsonify({"status": "updated", "quantity": item.quantity})

    @app.get("/reorder/export-pdf")
    def reorder_export_pdf():
        """Generate and return a PDF of the current reorder list."""
        items = ReorderListItem.query.order_by(ReorderListItem.added_at).all()
        if not items:
            abort(404)

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)

        styles = getSampleStyleSheet()
        subtitle_style = ParagraphStyle("subtitle", parent=styles["Normal"],
                                        textColor=colors.HexColor("#64748b"), fontSize=9)

        title = Paragraph("Reorder Request", styles["Title"])
        today = date.today()
        date_str = f"Generated: {today.day} {today.strftime('%B %Y')}"
        generated = Paragraph(date_str, subtitle_style)
        spacer = Spacer(1, 6*mm)

        total = sum(item.quantity for item in items)
        header = ["SKU", "Product Name", "Category", "Qty to Order"]
        data_rows = [
            [item.product.sku, item.product.name, item.product.category, str(item.quantity)]
            for item in items
        ]
        summary_row = ["", f"Total Units to Order: {total}", "", ""]
        rows = [header] + data_rows + [summary_row]

        last = len(rows) - 1
        col_widths = [30*mm, 75*mm, 45*mm, 25*mm]
        table = Table(rows, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTNAME", (0, 1), (-1, last - 1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, last - 1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, last - 1), [colors.white, colors.HexColor("#f8fafc")]),
            ("GRID", (0, 0), (-1, last - 1), 0.5, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            # Summary row styling
            ("SPAN", (1, last), (3, last)),
            ("FONTNAME", (0, last), (-1, last), "Helvetica-Bold"),
            ("FONTSIZE", (0, last), (-1, last), 9),
            ("TOPPADDING", (0, last), (-1, last), 6),
            ("LINEABOVE", (0, last), (-1, last), 1, colors.HexColor("#1e293b")),
            ("BACKGROUND", (0, last), (-1, last), colors.HexColor("#f1f5f9")),
        ]))

        try:
            doc.build([title, generated, spacer, table])
        except Exception:
            return jsonify({"status": "error", "message": "Failed to generate PDF"}), 500
        buf.seek(0)
        return send_file(buf, mimetype="application/pdf",
                         download_name="reorder-list.pdf", as_attachment=True)

    @app.delete("/reorder/remove/<int:product_id>")
    def reorder_remove(product_id: int):
        """Remove a product from the reorder list."""
        item = ReorderListItem.query.filter_by(product_id=product_id).first()
        if item is None:
            abort(404)
        db.session.delete(item)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return jsonify({"status": "error", "message": "Failed to remove item"}), 500
        return jsonify({"status": "removed", "count": ReorderListItem.query.count()})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
