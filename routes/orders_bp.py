
from flask import Blueprint, request
from extensions import db
from models.cart import Cart
from models.product import Product
from models.order import Order, OrderItem
from datetime import datetime

orders_bp = Blueprint("orders_bp", __name__)


#  Place order (checkout)
@orders_bp.post("/orders/<int:user_id>")
def place_order(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return {"error": "Cart is empty"}, 400

    data = request.get_json()

    # 1. Group cart items by seller
    items_by_seller = {}
    for item in cart_items:
        seller_id = item.product.user_id
        if seller_id not in items_by_seller:
            items_by_seller[seller_id] = []
        items_by_seller[seller_id].append(item)

    created_orders = []

    try:
        # 2. Create one order per seller
        for seller_id, items in items_by_seller.items():
            total_price = sum(item.product.price * item.count for item in items)

            order = Order(
                user_id=user_id,
                total_price=total_price,
                name=data.get("name"),
                phone=data.get("phone"),
                pincode=data.get("pincode"),
                locality=data.get("locality"),
                address=data.get("address"),
                city=data.get("city"),
                state=data.get("state"),
                landmark=data.get("landmark"),
                altphone=data.get("altphone"),
            )
            db.session.add(order)
            db.session.commit()

            # Add order items
            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.count,
                    price=item.product.price,
                )
                db.session.add(order_item)

            created_orders.append(order.to_dict())

        # 3. Clear the user's cart
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return {"orders": created_orders}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500



#  Buyer: get all orders for a user
@orders_bp.get("/orders/<int:user_id>")
def get_orders_for_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return [o.to_dict() for o in orders], 200


#  Seller: get all orders for a product
@orders_bp.get("/orders/product/<int:product_id>")
def get_orders_for_product(product_id):
    orders = Order.query.join(OrderItem).filter(OrderItem.product_id == product_id).all()
    return [o.to_dict() for o in orders], 200


#  Admin: get all orders
@orders_bp.get("/admin/orders")
def get_all_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return [o.to_dict() for o in orders], 200


# #  Update order status
@orders_bp.put("/orders/<int:order_id>")
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
        if status == "completed":
            order.delivery_date = datetime.now()  # <-- set delivery date
        else:
            order.delivery_date = None  # reset if not completed

        db.session.commit()
        return order.to_dict(), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500




@orders_bp.get("/orders/seller/<int:seller_id>")
def get_orders_for_seller(seller_id):
    orders = (
        Order.query.join(OrderItem).join(Product)
        .filter(Product.user_id == seller_id)  # only seller's products
        .order_by(Order.created_at.desc())
        .all()
    )
    return [o.to_dict() for o in orders], 200
