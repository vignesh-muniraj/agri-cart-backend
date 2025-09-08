from flask import Blueprint, request
from extensions import db
from models.product import Product

products_bp = Blueprint("products_bp", __name__)

# GET all products
@products_bp.get("/products")
def get_products():
    products = [p.to_dict() for p in Product.query.all()]
    return products, 200  

# GET single product by id
@products_bp.get("/products/<int:product_id>")
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404
    return product.to_dict(), 200

# POST new product
@products_bp.post("/products")
def add_product():
    data = request.get_json()
    if not data:
        return {"error": "No input data provided"}, 400

    try:
        product = Product(
            name=data.get("name"),
            poster=data.get("poster"),
            price=data.get("price"),
            category=data.get("category"),
            quantity=data.get("quantity"),
        )
        db.session.add(product)
        db.session.commit()
        return product.to_dict(), 201  
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
