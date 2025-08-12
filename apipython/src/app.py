from flask import Flask
from flask_cors import CORS  # <--- Importa CORS
from src.routes.main import bp as api_bp

def create_app():
    app = Flask(__name__)

    CORS(app) 
    app.register_blueprint(api_bp)
    return app
