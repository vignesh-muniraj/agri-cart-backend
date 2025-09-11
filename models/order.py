from extensions import db
from datetime import datetime

# class Order(db.Model):
#     __tablename__ = "orders"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     total_price = db.Column(db.Numeric, nullable=False)
#     status = db.Column(db.String(50), default="pending")  # pending, completed, cancelled
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

#     user = db.relationship("User", backref="orders")

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "username": self.user.username if self.user else None,
#             "total_price": str(self.total_price),
#             "status": self.status,
#             "created_at": self.created_at,
#             "items": [item.to_dict() for item in self.items],
#         }



class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    locality = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    landmark = db.Column(db.String(200), nullable=True)
    altphone = db.Column(db.String(15), nullable=True)

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")
    user = db.relationship("User", backref="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_price": str(self.total_price),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "name": self.name,
            "phone": self.phone,
            "pincode": self.pincode,
            "locality": self.locality,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "landmark": self.landmark,
            "altphone": self.altphone,
            "items": [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric, nullable=False)  # snapshot price

    product = db.relationship("Product")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "quantity": self.quantity,
            "price": str(self.price),
        }