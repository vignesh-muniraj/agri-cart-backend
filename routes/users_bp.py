from flask import Blueprint, request
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

HTTP_NOT_FOUND = 404
HTTP_CREATED = 201
HTTP_ERROR = 500

users_bp = Blueprint("users_bp", __name__)

@users_bp.get("/")
def get_all_users():
    users = [user.to_dict() for user in User.query.all()]
    return users

@users_bp.post("/signup")
def create_user():
    data = request.get_json()  # body
    username = data.get("username")  # None (falsy) # postman
    password = data.get("password")  # "" (falsy) # postman

    if not username or not password:
        return {"error": "username / password required"}, 400

    db_user = User.query.filter_by(username=username).first()  # None

    if db_user:
        return {"error": "username already taken"}, 400

    new_user = User(username=username, password=generate_password_hash(password))  # id
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Sign Up Successful"}, HTTP_CREATED
    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_ERROR


@users_bp.post("/login")
def login_user():
    data = request.get_json()
    username = data.get("username")  # None (falsy) # postman
    password = data.get("password")  # "" (falsy) # postman

    # 🛡️ Shielding
    if not username or not password:
        return {"error": "username / password required"}, 400

    db_user = User.query.filter_by(username=username).first()  # None
    # print("🚚🚚🚚🚚🚚🚚🚚")
    print(db_user)
    # No User found in DB
    if not db_user:
        return {"error": "username or password is incorrect"}, 401

    # User ✅ but Password?
    db_user = db_user.to_dict()
    print("🚚🚚🚚🚚🚚🚚🚚")
    print(db_user)
    # Password Check
    if not check_password_hash(db_user.get("password"), password):
        return {"error": "username or password is ❓incorrect"}, 401
    
    token = create_access_token(identity=username)
    # Password ✅, Token Generated ✅
    return {"message": "Login Up Successful", "token": token}