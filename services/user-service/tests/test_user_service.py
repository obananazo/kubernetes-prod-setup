# ------------------------------ Happy Paths ------------------------------


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_register_success(register_user):
    response = register_user(full_name="Test User")
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_login_success(client, register_user, user_password):
    register_user()
    response = client.post(
        "/login", json={"email": "test@example.com", "password": user_password}
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_me_with_token(client, auth_headers):
    response = client.get("/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["email"] == "test@example.com"


# ------------------------------ Error Cases ------------------------------


def test_login_wrong_password(client, register_user):
    register_user()
    response = client.post(
        "/login", json={"email": "test@example.com", "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_register_duplicate_username(register_user):
    register_user()
    response = register_user(email="another@example.com")  # same username, new email
    assert response.status_code == 400
    assert response.json["error"] == "Username or email already exists"


def test_register_duplicate_email(register_user):
    register_user()
    response = register_user(username="anotheruser")  # same email, new username
    assert response.status_code == 400
    assert response.json["error"] == "Username or email already exists"


def test_register_missing_fields(client):
    response = client.post("/register", json={"email": "test@example.com"})
    assert response.status_code == 400
    assert response.json["error"] == "Missing required fields"


def test_me_requires_auth(client):
    response = client.get("/me")
    assert response.status_code == 401


def test_me_with_invalid_token(client):
    response = client.get("/me", headers={"Authorization": "Bearer invalid"})
    assert (
        response.status_code == 422
    )  # Flask-JWT-Extended returns 422 for invalid tokens, not 401


def test_login_unknown_user(client):
    response = client.post(
        "/login", json={"email": "nobody@example.com", "password": "whatever"}
    )
    assert response.status_code == 401


# ------------------------------ Edge Cases ------------------------------


def test_register_without_json_body(client):
    response = client.post("/register")
    assert response.status_code == 415


def test_register_empty_strings(client):
    response = client.post(
        "/register", json={"email": "", "username": "", "password": ""}
    )
    assert response.status_code == 400
