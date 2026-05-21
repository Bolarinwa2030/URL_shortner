from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

# Use the DATABASE_URL from environment (set in CI workflow)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/testdb")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables before tests run
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the database dependency with test database
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200


def test_shorten_url_returns_short_code():
    response = client.post(
        "/api/v1/shorten", json={"original_url": "https://google.com"}
    )
    assert response.status_code == 200
    assert "short_url" in response.json()


def test_missing_short_code_returns_404():
    response = client.get("/doesnotexist999")
    assert response.status_code == 404
