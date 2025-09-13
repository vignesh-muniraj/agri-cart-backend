from flask import Blueprint, request,jsonify
from models.user import User
from extensions import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

HTTP_ERROR = 500

users_bp = Blueprint("users_bp", __name__)

@users_bp.post("/login")
def login_user():
    data = request.get_json()
    id = data.get("id")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    seller_or_buyer = data.get("seller_or_buyer")

    if not username or not password:
        return {"error": "Username and password required"}, 400

    db_user = User.query.filter_by(username=username).first()
    if not db_user:
        return {"error": "Invalid username or password"}, 401

    if not check_password_hash(db_user.password, password):
        return {"error": "Invalid username or password"}, 401

    token = create_access_token(identity=username)
    # return {"message": "Login Successful", "token": token,"username":db_user.username,"id":db_user.id}
    return {
        "message": "Login Successful",
        "token": token,
        "user": db_user.to_dict()
    }


# user_bp = Blueprint("user_b", __name__)

@users_bp.route("/  /<int:user_id>", methods=["PUT"])
def become_seller(user_id):
    data = request.json
    aadhar_no = data.get("aadhar_no")

    if not aadhar_no or len(aadhar_no) != 12:
        return jsonify({"error": "Valid 12-digit Aadhaar number required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.aadhar_no = aadhar_no
    user.seller_or_buyer = "seller"
    db.session.commit()

    return jsonify({"message": "You are now a seller", "user": user.to_dict()})
