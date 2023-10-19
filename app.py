from flask import Flask
from routes.route import face
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(face)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

if __name__ == "__main__":
    app.run(debug=True, port=5000)