from app.extensions import db
from app.infrastructure.database.models import Owner
from app.presentation.rest.schemas import validate_owner_data


def create_owner_service(data):
    validated_data, errors = validate_owner_data(data)

    if errors:
        return None, errors

    new_owner = Owner(
        name=validated_data["name"],
        sale_opportunity=validated_data.get("sale_opportunity"),
    )

    db.session.add(new_owner)
    db.session.commit()

    return new_owner, None


def update_sales_opportunity_service(owner):
    owner.sales_opportunity = not owner.cars
    db.session.commit()

