from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200

def test_add_product():
    response = client.post(
        "/products",
        json={
            "id": 52,
            "name": "Phone",
            "description": "Budget Phone",
            "price": 100,
            "quantity": 5
        }
    )
    assert response.status_code == 200

def test_unauthorized_product():
    response = client.get("/products/999")
    assert response.status_code == 401
