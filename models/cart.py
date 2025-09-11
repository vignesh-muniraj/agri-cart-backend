# from extensions import db

from extensions import db
# from models.product import Product


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    price = db.Column(db.Numeric, nullable=False)  # must pass price
    quantity = db.Column(db.String(50))
    count = db.Column(db.Integer, default=1)

    product = db.relationship("Product", backref="cart_items")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "name": self.product.name if self.product else None,
            "poster": self.product.poster if self.product else None,
            "price": str(self.price) if self.price else None,
            "quantity": self.quantity,
            "count": self.count,
        }
