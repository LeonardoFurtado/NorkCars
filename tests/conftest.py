import os
import tempfile
import pytest
from app import create_app
from app.extensions import db, bcrypt
from app.infrastructure.database.models import Owner, Car, User


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(db=f"sqlite:///{db_path}")

    with app.app_context():
        yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def init_database(app):
    """Create the database and tables."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.rollback()
        db.drop_all()


@pytest.fixture
def random_owner(init_database):
    payload = {
        "name": "Harry Potter",
    }
    record = Owner(**payload)
    db.session.add(record)
    db.session.commit()
    return record


@pytest.fixture
def another_random_owner(init_database):
    payload = {
        "name": "Sirius Black",
    }
    record = Owner(**payload)
    db.session.add(record)
    db.session.commit()
    return record


@pytest.fixture
def random_car(init_database, random_owner):
    payload = {
        "color": "yellow",
        "model": "sedan",
        "owner_id": random_owner.id,
    }
    record = Car(**payload)
    db.session.add(record)
    db.session.commit()
    return record


@pytest.fixture
def another_random_car(init_database, random_owner):
    payload = {
        "color": "gray",
        "model": "hatch",
        "owner_id": random_owner.id,
    }
    record = Car(**payload)
    db.session.add(record)
    db.session.commit()
    return record


@pytest.fixture
def car_from_another_owner(init_database, another_random_owner):
    payload = {
        "color": "blue",
        "model": "sedan",
        "owner_id": another_random_owner.id,
    }
    record = Car(**payload)
    db.session.add(record)
    db.session.commit()
    return record

@pytest.fixture
def create_test_user(init_database):
    """Fixture to create a test user."""
    username = "testuser"
    password = "password123"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_token(client, create_test_user):
    """Fixture to retrieve JWT token for authentication."""
    username = "testuser"
    password = "password123"

    response = client.post("/login", json={"username": username, "password": password})
    return response.json.get("access_token")
