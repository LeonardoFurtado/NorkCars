from flask import Flask
from app.extensions import init_app
import secrets

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://carford:carfordpass@db/carforddb"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# JWT_SECRET_KEY = secrets.token_urlsafe(32)
# app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY




def create_app(db=None):
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    if db:
        app.config["SQLALCHEMY_DATABASE_URI"] = db
    init_app(app)
    from .views import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
