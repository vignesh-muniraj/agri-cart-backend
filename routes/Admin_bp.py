from flask import Blueprint, jsonify
from models.user import User
from models.product import Product
from models.order import Order   # assuming you have this
from extensions import db

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/users", methods=["GET"])
def get_all_users_with_stats():
    users = User.query.all()
    result = []
    for u in users:
        # count products (as seller)
        product_count = Product.query.filter_by(seller_id=u.id).count()

        # count orders (as buyer)
        order_count = Order.query.filter_by(user_id=u.id).count()

        result.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "seller_or_buyer": u.seller_or_buyer,
            "aadhar_no": u.aadhar_no,
            "products_count": product_count,
            "orders_count": order_count
        })
    return jsonify(result)




# Delete a user by ID (admin only)
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})