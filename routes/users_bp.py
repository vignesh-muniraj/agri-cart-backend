from flask import Blueprint, request
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
