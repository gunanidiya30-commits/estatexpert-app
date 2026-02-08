from flask import Flask
from backend.routes.core.routes import core_bp
from backend.routes.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "estatexpert-secret-key"

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)

    return app
