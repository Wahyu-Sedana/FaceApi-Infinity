echo "from flask import Flask" > app.py
echo "from routes.route import face" >> app.py
echo "from flask_cors import CORS" >> app.py
echo "" >> app.py
echo "app = Flask(__name__)" >> app.py
echo "app.register_blueprint(face)" >> app.py
echo "CORS(app, resources={r\"/*\": {\"origins\": \"https://absensi-staging.infinityprogress.id\"}})" >> app.py
echo "app.config['CORS_SUPPORTS_CREDENTIALS'] = True" >> app.py
echo "" >> app.py
echo "if __name__ == \"__main__\":" >> app.py
echo "    app.run(debug=True, port=5000)" >> app.py