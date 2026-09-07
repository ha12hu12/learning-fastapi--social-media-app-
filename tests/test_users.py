import pytest
from app import schemas
from app.config import settings
from jose import jwt

def test_create_user(client):
    res = client.post("/users/", json={
        "email": "hussein123456@gmail.com",
        "password": "hussein13pas"
    })

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hussein123456@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'],
                                      "password": test_user['password']})

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('ha12hu12@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('ha12hu12@gmail.com', None, 422)
] )
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": password})

    assert res.status_code == status_code