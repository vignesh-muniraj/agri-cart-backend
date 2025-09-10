from flask import Blueprint, request
from extensions import db
from models.cart import Cart
from models.product import Product

cart_bp = Blueprint("cart_bp", __name__)


# ✅ GET all cart items for a user
@cart_bp.get("/cart/<int:user_id>")
def get_cart(user_id):
    cart_items = [c.to_dict() for c in Cart.query.filter_by(user_id=user_id).all()]
    return cart_items, 200


# ✅ POST add item to cart
@cart_bp.post("/cart")
def add_to_cart():
    data = request.get_json()
    if not data:
        return {"error": "No input data provided"}, 400

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", "500g")

    # ✅ Get the product to fetch price
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    # ✅ Check if already in cart (same user + same product + same quantity)
    existing_cart = Cart.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    ).first()

    if existing_cart:
        return {"message": f"{product.name} is already in your cart"}, 200

    try:
        cart_item = Cart(
            user_id=user_id,
            product_id=product.id,
            price=product.price,   # ✅ take from product table
            quantity=quantity,
            count=data.get("count", 1),
        )
        db.session.add(cart_item)
        db.session.commit()
        return cart_item.to_dict(), 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500



# ✅ PUT update cart item count
@cart_bp.put("/cart/<int:cart_id>")
def update_cart(cart_id):
    data = request.get_json()
    cart_item = Cart.query.get(cart_id)

    if not cart_item:
        return {"error": "Cart item not found"}, 404

    try:
        cart_item.count = data.get("count", cart_item.count)
        db.session.commit()
        return cart_item.to_dict(), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# ✅ DELETE cart item
@cart_bp.delete("/cart/<int:cart_id>")
def delete_cart(cart_id):
    cart_item = Cart.query.get(cart_id)

    if not cart_item:
        return {"error": "Cart item not found"}, 404

    try:
        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Cart item deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
