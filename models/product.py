from extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    poster = db.Column(db.String(300))
    price = db.Column(db.Numeric, nullable=False)
    category = db.Column(db.String(100))
    quantity = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "price": self.price,
            "category": self.category,
            "quantity": self.quantity,
            "user_id": self.user_id,
        }
