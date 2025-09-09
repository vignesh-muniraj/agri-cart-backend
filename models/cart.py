from extensions import db

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    # name = db.Column(db.String, nullable=False)
    # poster = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.String(50))
    count = db.Column(db.String(50),default = 1 )
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            # "name": self.name,
            # "poster": self.poster,
            "price": self.price,
            "quantity": self.quantity,
            "count":self.count
        }
