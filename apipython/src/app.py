from flask import Flask
from .config import load_env
from .routes.main import bp as main_bp
from flask_cors import CORS

def create_app():
    load_env()  
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(main_bp)
    return app
