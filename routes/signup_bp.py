from flask import Blueprint, request
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

HTTP_CREATED = 201
HTTP_ERROR = 500

signup_bp = Blueprint("signup_bp", __name__)

@signup_bp.post("/signup")
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "All fields are required"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already taken"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}, 400

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        token = create_access_token(identity=username)
        return {"message": "Sign Up Successful", "token": token}, 201
    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, 500
