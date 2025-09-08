# from extensions import db

# class Cart(db.Model):
#     __tablename__ = "cart"
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.String(50), nullable=False)
#     name = db.Column(db.String(150), nullable=False)
#     poster = db.Column(db.String(300))
#     price = db.Column(db.Float, nullable=False)
#     category = db.Column(db.String(100))
#     quantity = db.Column(db.String(50), default="1")  # e.g., "500g"

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "product_id": self.product_id,
#             "name": self.name,
#             "poster": self.poster,
#             "price": self.price,
#             "category": self.category,
#             "quantity": self.quantity,
#         }
