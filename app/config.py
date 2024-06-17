import os
import secrets


class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://carford:carfordpass@db/carforddb"
    JWT_SECRET_KEY = secrets.token_urlsafe(32)

