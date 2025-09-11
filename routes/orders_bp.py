from flask import Blueprint, request
from extensions import db
from models.cart import Cart
from models.product import Product
from models.order import Order, OrderItem

orders_bp = Blueprint("orders_bp", __name__)


# ✅ Place order (checkout)
@orders_bp.post("/orders/<int:user_id>")
def place_order(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return {"error": "Cart is empty"}, 400

    data = request.get_json()  # read address info from frontend

    total_price = sum(item.product.price * item.count for item in cart_items)

    try:
        # create order with address info
        order = Order(
            user_id=user_id,
            total_price=total_price,
            name=data.get("name"),
            phone=data.get("phone"),
            pincode=data.get("pincode"),
            locality=data.get("locality") or None,
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            landmark=data.get("landmark") or None,
            altphone=data.get("altphone") or None,
        )
        db.session.add(order)
        db.session.commit()  # commit to get order.id

        # create order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.count,
                price=item.product.price,
            )
            db.session.add(order_item)

        # clear the cart
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return order.to_dict(), 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


# ✅ Get order history for a user
@orders_bp.get("/orders/<int:user_id>")
def get_orders(user_id):
    orders = (
        Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    )
    return [o.to_dict() for o in orders], 200


# ✅ Admin: Get all orders
@orders_bp.get("/admin/orders")
def get_all_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return [o.to_dict() for o in orders], 200


# ✅ Admin: Update order status
@orders_bp.put("/admin/orders/<int:order_id>")
def update_order_status(order_id):
    data = request.get_json()
    status = data.get("status")
    if status not in ["pending", "completed", "cancelled"]:
        return {"error": "Invalid status"}, 400

    order = Order.query.get(order_id)
    if not order:
        return {"error": "Order not found"}, 404

    try:
        order.status = status
        db.session.commit()
        return order.to_dict(), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
