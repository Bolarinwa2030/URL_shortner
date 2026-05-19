import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shorten_url_returns_short_code():
    response = client.post("/api/v1/shorten", json={
        "original_url": "https://google.com"
    })
    assert response.status_code == 200
    assert "short_url" in response.json()

def test_redirect_follows_to_original():
    # Create a known short code
    client.post("/api/v1/shorten", json={
        "original_url": "https://example.com",
        "custom_alias": "testme"
    })
    resp = client.get("/testme", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["location"] == "https://example.com"

def test_missing_short_code_returns_404():
    resp = client.get("/doesnotexist999")
    assert resp.status_code == 404