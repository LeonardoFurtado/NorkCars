from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    sale_opportunity = db.Column(db.Boolean, default=True)
    cars = db.relationship("Car", backref="owner", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sale_opportunity": self.sale_opportunity,
            "cars": self.cars,
        }


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=False)

    def __init__(self, color, model, owner_id):
        if color not in ["yellow", "blue", "gray"]:
            raise ValueError("Invalid color. Only 'yellow', 'blue', and 'gray' are allowed.")
        if model not in ["hatch", "sedan", "convertible"]:
            raise ValueError("Invalid model. Only 'hatch', 'sedan', and 'convertible' are allowed.")
        self.color = color
        self.model = model
        self.owner_id = owner_id

    def to_dict(self):
        return {
            "id": self.id,
            "color": self.color,
            "model": self.model,
            "owner_id": self.owner_id,
        }
