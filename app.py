from flask import Flask
from routes.route import face

app = Flask(__name__)
app.register_blueprint(face)


if __name__ == "__main__":
    app.run(debug=True, port=5000)