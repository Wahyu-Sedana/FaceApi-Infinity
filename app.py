from flask import Flask
from routes.route import face
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://absensi-staging.infinityprogress.id"}})
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.register_blueprint(face)

if __name__ == "__main__":
    app.run(debug=True, port=5000)