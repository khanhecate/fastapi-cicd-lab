from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_item():
    item = {"id": 1, "name": "Coffee", "price": 4.5}
    create_response = client.post("/items", json=item)
    assert create_response.status_code == 201

    get_response = client.get("/items/1")
    assert get_response.status_code == 200
    assert get_response.json() == item


def test_get_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404