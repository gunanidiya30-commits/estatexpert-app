from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "EstateXpert backend is running"

    return app
