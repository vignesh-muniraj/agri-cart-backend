
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from routes.signup_bp import signup_bp
from routes.users_bp import users_bp
from routes.products_bp import products_bp
from routes.cart_bp  import cart_bp 
from routes.orders_bp  import orders_bp 
# from routes.cart_bp import cart_bp
from os import environ

app = Flask(__name__)
app.config.from_object("config.Config")
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
jwt.init_app(app)

@app.get("/")
def hello_world():
    print("Super")
    return "<h1>Hello, World! 🎊🍊 🌽</h1>"

app.register_blueprint(signup_bp, url_prefix="/users")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp )
app.register_blueprint(orders_bp)
# app.register_blueprint(cart_bp, url_prefix="/api")


if __name__ == "__main__":
    port = environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=True)

