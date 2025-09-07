from config import Config
from flask import Flask
from flask_cors import CORS
from extensions import db,jwt
from sqlalchemy.sql import text
from os import environ

app = Flask(__name__)
app.config.from_object(Config)  # URL
CORS(app)
# CORS(app,
#      resources={r"/*": {"origins": "http://localhost:5173"}},
#      supports_credentials=True,
#      allow_headers=["Content-Type", "Authorization"],
#      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])


db.init_app(app)  # Call
jwt.init_app(app)

with app.app_context():
    try:
        result = db.session.execute(text("SELECT 3")).fetchall()
        print("Connection successful:", result)
    except Exception as e:
        print("Error connecting to the database:", e)


@app.get("/")
def hello_world():
    print("Super")
    return "<h1>Hello, World! 🎊🍊 🌽</h1>"


from routes.users_bp import users_bp

app.register_blueprint(users_bp,url_prefix="/users")

if __name__ == "__main__":
    port = environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=True)