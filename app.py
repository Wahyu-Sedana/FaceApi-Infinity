from routes.route import face
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config.database import mysql

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_DATABASE")

mysql.init_app(app)

app.register_blueprint(face)
CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
