from fastapi.testclient import TestClient

from app.config import parse_cors_origins
from app.main import app


def test_cors_origins_are_normalized():
    assert parse_cors_origins("(https://example.vercel.app/), https://example.test/") == [
        "https://example.vercel.app",
        "https://example.test",
    ]


def test_health_and_products():
    with TestClient(app) as client:
        health = client.get("/")
        assert health.status_code == 200
        assert health.json()["eligible_products"] == 104
        products = client.get("/products")
        assert products.status_code == 200
        assert len(products.json()) == 104


def test_recommend_validates_empty_input_and_respects_budget():
    with TestClient(app) as client:
        assert client.post("/recommend", json={"occasion": "   "}).status_code == 422
        response = client.post("/recommend", json={"occasion": "Something under ₹1000", "top_k": 10})
        assert response.status_code == 200
        result = response.json()
        assert result["recommendations"]
        assert all(item["price"] <= 1000 for item in result["recommendations"])
