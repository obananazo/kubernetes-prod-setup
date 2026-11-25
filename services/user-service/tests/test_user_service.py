def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_register_success(client):
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_register_missing_fields(client):
    response = client.post("/register", json={"email": "test@example.com"})
    assert response.status_code == 400
    assert response.json["error"] == "Missing required fields"


def test_register_duplicate_email(client):
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
        },
    )
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "anotheruser",
            "password": "secret123",
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "Username or email already exists"


def test_login_success(client):
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
        },
    )
    response = client.post(
        "/login", json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_wrong_password(client):
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
        },
    )
    response = client.post(
        "/login", json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/me")
    assert response.status_code == 401


def test_me_with_token(client):
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123",
            "full_name": "Test User",
        },
    )
    login = client.post(
        "/login", json={"email": "test@example.com", "password": "secret123"}
    )
    token = login.json["access_token"]

    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json["email"] == "test@example.com"
