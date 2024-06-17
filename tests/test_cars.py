def test_post_car_should_success(client, init_database, random_owner, auth_token):
    data = {
        "color": "yellow",
        "model": "sedan",
        "owner_id": random_owner.id,
    }
    response = client.post("/cars", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201


def test_post_car_without_owner_id_should_fail(client, init_database, auth_token):
    data = {
        "color": "yellow",
        "model": "sedan",
    }
    response = client.post("/cars", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400


def test_post_car_without_color_should_fail(client, init_database, random_owner, auth_token):
    data = {
        "model": "sedan",
        "owner_id": random_owner.id,
    }
    response = client.post("/cars", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400


def test_post_car_without_model_should_fail(client, init_database, random_owner, auth_token):
    data = {
        "color": "yellow",
        "owner_id": random_owner.id,
    }
    response = client.post("/cars", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400


def test_get_car_by_id(client, init_database, random_car, auth_token):
    response = client.get(f"/cars/{random_car.id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json == random_car.to_dict()


def test_should_return_all_cars_from_a_owner(
    client,
    init_database,
    random_car,
    another_random_car,
    random_owner,
    car_from_another_owner,
auth_token):
    response = client.get(f"/owners/{random_owner.id}/cars", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert len(response.json) == 2


def test_should_return_all_cars(
    client,
    init_database,
    random_car,
    another_random_car,
    car_from_another_owner,
auth_token):
    response = client.get(f"/cars", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert len(response.json) == 3


def test_should_delete_car(client, init_database, random_car, auth_token):
    response = client.delete(f"/cars/{random_car.id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 204
    response = client.get(f"/cars/{random_car.id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404


def test_should_fail_update_car_with_wrong_color(client, init_database, random_car, auth_token):
    response = client.patch(f"/cars/{random_car.id}", json={"color": "red"}, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400
    assert response.json["error"] == "Invalid color. Only 'yellow', 'blue', and 'gray' are allowed."


def test_should_update_car_with_color(client, init_database, random_car, auth_token):
    response = client.patch(f"/cars/{random_car.id}", json={"color": "blue"}, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
