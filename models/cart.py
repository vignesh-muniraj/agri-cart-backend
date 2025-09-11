from extensions import db

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    count = db.Column(db.Integer, default=1)

    # relationship to product
    product = db.relationship("Product", back_populates="carts")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "count": self.count,
            # pull details live from product
            "name": self.product.name if self.product else None,
            "poster": self.product.poster if self.product else None,
            "price": str(self.product.price) if self.product else None,
            "quantity": self.product.quantity if self.product else None,
            "category": self.product.category if self.product else None,
        }
