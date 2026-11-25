import os

import pytest

# Must be set before the app is imported, otherwise the engine uses the real DB
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import Base, engine  # noqa: E402, RUF100
from app.main import app as flask_app  # noqa: E402, RUF100

TEST_PASSWORD = "secret123"


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = (
        "test-secret-key-that-is-long-enough-32-characters"
    )
    Base.metadata.create_all(bind=engine)
    yield flask_app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def register_user(client):
    def _register(email="test@example.com", username="testuser", **extra):
        return client.post(
            "/register",
            json={
                "email": email,
                "username": username,
                "password": TEST_PASSWORD,
                **extra,
            },
        )

    return _register


@pytest.fixture
def auth_headers(client, register_user):
    register_user()
    response = client.post(
        "/login",
        json={"email": "test@example.com", "password": TEST_PASSWORD},
    )
    return {"Authorization": f"Bearer {response.json['access_token']}"}


@pytest.fixture
def user_password():
    return TEST_PASSWORD
