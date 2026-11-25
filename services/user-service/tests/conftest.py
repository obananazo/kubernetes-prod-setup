import os

import pytest

# Must be set before the app is imported, otherwise the engine uses the real DB
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import Base, engine  # noqa: E402, RUF100
from app.main import app as flask_app  # noqa: E402, RUF100


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
