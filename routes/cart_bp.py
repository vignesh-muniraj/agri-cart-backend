# from flask import Blueprint, request, jsonify
# from models.cart import Cart
# from extensions import db

# HTTP_CREATED = 201
# HTTP_ERROR = 500

# cart_bp = Blueprint("cart_bp", __name__)

# # Get all cart items
# @cart_bp.get("/cart")
# def get_cart_items():
#     items = [item.to_dict() for item in Cart.query.all()]
#     return jsonify(items)

# # Add item to cart
# @cart_bp.post("/cart")
# def add_cart_item():
#     data = request.get_json()
#     new_item = Cart(
#         product_id=data.get("id"),
#         name=data.get("name"),
#         poster=data.get("poster"),
#         price=data.get("price"),
#         category=data.get("category"),
#         quantity=data.get("quantity", "1")
#     )
#     try:
#         db.session.add(new_item)
#         db.session.commit()
#         return jsonify({"message": "Item added to cart"}), HTTP_CREATED
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), HTTP_ERROR

# # Delete item from cart
# @cart_bp.delete("/cart/<int:id>")
# def delete_cart_item(id):
#     item = Cart.query.get(id)
#     if not item:
#         return jsonify({"error": "Item not found"}), 404
#     try:
#         db.session.delete(item)
#         db.session.commit()
#         return jsonify({"message": "Item deleted"})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), HTTP_ERROR
