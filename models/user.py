# models/user.py
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(100), default="USER")
    password = db.Column(db.String(255), nullable=False)

    # relationships
    products = db.relationship("Product", backref="seller", lazy=True)
    carts = db.relationship("Cart", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "password": self.password,   # ⚠️ usually don’t send password, but kept for you
        }
