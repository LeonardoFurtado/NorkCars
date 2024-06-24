def test_create_owner_should_success(client, init_database, auth_token):
    data = {"name": "Harry Potter"}
    response = client.post("/owners", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201


def test_create_owner_should_fail_if_name_not_provided(client, init_database, auth_token):
    data = {}
    response = client.post("/owners", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400
    assert response.json["error"] == {"name": ["Missing data for required field."]}


def test_should_return_owner_by_id(client, init_database, random_owner, auth_token):
    response = client.get("/owners/1", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200


def test_get_should_return_404_if_owner_id_dont_exist(
    client, init_database, random_owner
, auth_token):
    response = client.get("/owners/9999999", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404


def test_should_update_owner(client, init_database, random_owner, auth_token):
    data = {"name": "Harry But Not Potter"}
    response = client.patch("/owners/1", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json["name"] == data["name"]


def test_patch_should_return_404_if_owner_doesnt_exist(client, init_database, auth_token):
    data = {"name": "Harry But Not Potter"}
    response = client.patch("/owners/94589485", json=data, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404


def test_should_delete_owner(client, init_database, random_owner, auth_token):
    response = client.delete("/owners/1", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 204
    response = client.get("/owners/1", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404


def test_delete_should_return_404_if_owner_doesnt_exist(client, init_database, auth_token):
    response = client.delete("/owners/9999999", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404


def test_should_list_all_owners(client, init_database, random_owner, another_random_owner, auth_token):
    response = client.get("/owners", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert len(response.json) == 2


def test_should_return_owner_by_id_when_owner_have_cars(client, init_database, random_owner, auth_token, random_car):
    response = client.get("/owners/1", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200

