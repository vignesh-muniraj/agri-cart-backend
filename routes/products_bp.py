from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product
from sqlalchemy import or_


products_bp = Blueprint("products_bp", __name__)


# GET all products
@products_bp.get("/products")
def get_products():
    products = [p.to_dict() for p in Product.query.all()]
    return products, 200

# 🔎 Search products by name or descriptio
@products_bp.get("/products/search")
def search_products():
    q = request.args.get("q", "").strip()
    if not q:
        return {"products": []}, 200

    products = Product.query.filter(Product.name.ilike(f"%{q}%")).all()

    return {"products": [p.to_dict() for p in products]}, 200


# GET single product by id
@products_bp.get("/products/<int:product_id>")
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404
    return product.to_dict(), 200


# POST new product
@products_bp.post("/products")
def add_product():
    data = request.json
    try:
        new_product = Product(
            name=data["name"],
            poster=data["poster"],
            price=data["price"],
            category=data["category"],
            quantity=data["quantity"],
            user_id=data["user_id"],  # 👈 seller’s user_id comes here
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201
    except Exception as e:
        return {"error": str(e)}, 400


# /user dashboard


# GET products by seller (user_id)
@products_bp.get("/myproducts/<int:user_id>")
def get_my_products(user_id):
    products = Product.query.filter_by(user_id=user_id).all()
    return [p.to_dict() for p in products], 200


# PUT update product
@products_bp.put("/products/<int:id>")
def update_product(id):
    data = request.json
    product = Product.query.get(id)

    if not product:
        return {"error": "Product not found"}, 404

    # Update fields
    product.name = data.get("name", product.name)
    product.poster = data.get("poster", product.poster)
    product.price = data.get("price", product.price)
    product.category = data.get("category", product.category)
    product.quantity = data.get("quantity", product.quantity)
    # product.status = data.get("status", product.status)

    db.session.commit()
    return product.to_dict(), 200



@products_bp.put("/products/<int:id>/status")
def toggle_product_status(id):
    product = Product.query.get(id)
    if not product:
        return {"error": "Product not found"}, 404

    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["active", "inactive"]:
        return {"error": "Invalid status"}, 400

    product.status = new_status
    db.session.commit()
    return {
        "message": f"Product status updated to {new_status}",
        "status": product.status,
    }, 200


# DELETE product
@products_bp.delete("/products/<int:id>")
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return {"error": "Product not found"}, 404

    db.session.delete(product)
    db.session.commit()
    return {"message": "Product deleted successfully"}, 200


# 🔎 Search products by name or description
# @products_bp.route("/products/search")
# def search_products():
#     query = request.args.get("q", "").strip()

#     if not query:
#         return jsonify({"products": []}), 200

#     try:
#         results = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
#         products = [
#             {
#                 "id": p.id,
#                 "name": p.name,
#                 "price": str(p.price),
#                 "image": getattr(p, "poster", None),
#             }
#             for p in results
#         ]
#         return jsonify({"products": products}), 200

#     except Exception as e:
#         print("Search error:", e)
#         return jsonify({"error": str(e)}), 500
