from marshmallow import Schema, fields, validate, ValidationError


class OwnerSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    sale_opportunity = fields.Boolean(required=False, validate=validate.Length(min=1))


def validate_owner_data(data):
    schema = OwnerSchema()
    try:
        validated_data = schema.load(data)
        return validated_data, None
    except ValidationError as err:
        return None, err.messages


class CarSchema(Schema):
    color = fields.String(required=True, validate=validate.Length(min=1, max=20))
    model = fields.String(required=True, validate=validate.Length(min=1, max=20))
    owner_id = fields.Integer(required=True)


def validate_car_data(data):
    schema = CarSchema()
    try:
        validated_data = schema.load(data)
        return validated_data, None
    except ValidationError as err:
        return None, err.messages
