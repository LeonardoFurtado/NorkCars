from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from app.extensions import bcrypt, db
from app.infrastructure.database.models import User, Owner, Car
from app.service import create_owner_service, update_sales_opportunity_service

main = Blueprint("main", __name__)


@main.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # Verifica o usuário no banco de dados
    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    # Gera um token de acesso para o usuário autenticado
    access_token = create_access_token(identity={"username": username})
    return jsonify(access_token=access_token)


@main.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


# Cars
@main.route("/cars", methods=["POST"])
@jwt_required()
def add_car():
    data = request.get_json()
    color = data.get("color")
    model = data.get("model")
    owner_id = data.get("owner_id")

    if not all([color, model, owner_id]):
        return jsonify({"msg": "Missing parameters"}), 400

    if color not in ["yellow", "blue", "gray"]:
        return jsonify({"error": "Invalid color. Only 'yellow', 'blue', and 'gray' are allowed."}), 400

    if model not in ["hatch", "sedan", "convertible"]:
        return jsonify({"error": "Invalid model. Only 'hatch', 'sedan', and 'convertible' are allowed."}), 400

    owner = Owner.query.get(owner_id)
    if not owner:
        return jsonify({"msg": "Owner not found"}), 404

    new_car = Car(color=color, model=model, owner_id=owner_id)
    db.session.add(new_car)
    db.session.commit()
    update_sales_opportunity_service(owner)
    return jsonify({"msg": "Car added", "car_id": new_car.id}), 201


@main.route("/cars/<int:car_id>", methods=["GET"])
@jwt_required()
def get_car(car_id):
    car = Car.query.get(car_id)

    if not car:
        return jsonify({"error": "Car not found"}), 404

    return jsonify(car.to_dict()), 200


@main.route("/owners/<int:owner_id>/cars", methods=["GET"])
@jwt_required()
def get_owner_cars(owner_id):
    owner = Owner.query.get(owner_id)

    if not owner:
        return jsonify({"error": "Owner not found"}), 404

    cars = Car.query.filter_by(owner_id=owner_id).all()

    return jsonify([car.to_dict() for car in cars]), 200


@main.route("/cars", methods=["GET"])
@jwt_required()
def list_cars():
    cars = Car.query.all()
    return jsonify([car.to_dict() for car in cars])


@main.route("/cars/<int:car_id>", methods=["DELETE"])
@jwt_required()
def delete_car(car_id):
    car = Car.query.get(car_id)
    owner_id = car.owner_id
    owner = Owner.query.get(owner_id)

    if not car:
        return jsonify({"error": "Car not found"}), 404

    db.session.delete(car)
    db.session.commit()

    update_sales_opportunity_service(owner)
    return "", 204


@main.route("/cars/<int:car_id>", methods=["PATCH"])
@jwt_required()
def patch_car(car_id):
    data = request.get_json()
    car = Car.query.get(car_id)

    if not car:
        return jsonify({"error": "Car not found"}), 404

    if "color" in data:
        if data["color"] not in ["yellow", "blue", "gray"]:
            return jsonify({"error": "Invalid color. Only 'yellow', 'blue', and 'gray' are allowed."}), 400
        car.color = data["color"]

    if "model" in data:
        if data["model"] not in ["hatch", "sedan", "convertible"]:
            return jsonify({"error": "Invalid model. Only 'hatch', 'sedan', and 'convertible' are allowed."}), 400
        car.model = data["model"]

    if "owner_id" in data:
        owner = Owner.query.get(data["owner_id"])
        if not owner:
            return jsonify({"error": "Owner not found"}), 404
        car.owner_id = data["owner_id"]

    db.session.commit()

    return jsonify(car.to_dict()), 200


# Owners
@main.route("/owners", methods=["GET"])
@jwt_required()
def list_owners():
    owners = Owner.query.all()
    return jsonify([owner.to_dict() for owner in owners])


@main.route("/owners", methods=["POST"])
@jwt_required()
def create_owner():
    data = request.get_json()
    owner, error = create_owner_service(data)

    if error:
        return jsonify({"error": error}), 400

    return jsonify(owner.to_dict()), 201


@main.route("/owners/<int:owner_id>", methods=["GET"])
@jwt_required()
def get_owner(owner_id):
    owner = Owner.query.get(owner_id)

    if not owner:
        return jsonify({"error": "Owner not found"}), 404

    return jsonify(owner.to_dict()), 200


@main.route("/owners/<int:owner_id>", methods=["PATCH"])
@jwt_required()
def patch_owner(owner_id):
    data = request.get_json()
    owner = Owner.query.get(owner_id)

    if not owner:
        return jsonify({"error": "Owner not found"}), 404

    if "name" in data:
        owner.name = data["name"]

    if "sale_opportunity" in data:
        owner.sale_opportunity = data["sale_opportunity"]

    db.session.commit()

    return jsonify(owner.to_dict()), 200


@main.route("/owners/<int:owner_id>", methods=["DELETE"])
@jwt_required()
def delete_owner(owner_id):
    owner = Owner.query.get(owner_id)

    if not owner:
        return jsonify({"error": "Owner not found"}), 404

    db.session.delete(owner)
    db.session.commit()

    return "", 204


