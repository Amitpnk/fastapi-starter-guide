import pytest
from fastapi.testclient import TestClient

from app.items.dependencies import get_item_repository
from app.items.repository import InMemoryItemRepository
from app.main import app

ITEMS_URL = "/api/v1/items"


@pytest.fixture
def client():
    # Give every test its own empty repository so tests don't affect each other.
    repository = InMemoryItemRepository()
    app.dependency_overrides[get_item_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create(client, **overrides):
    body = {"name": "Laptop", "price": 999.99, **overrides}
    response = client.post(ITEMS_URL, json=body)
    assert response.status_code == 201
    return response.json()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_list_starts_empty(client):
    assert client.get(ITEMS_URL).json() == []


def test_create_item(client):
    item = create(client)
    assert item == {"id": 1, "name": "Laptop", "price": 999.99, "in_stock": True}


def test_get_item(client):
    item = create(client)
    response = client.get(f"{ITEMS_URL}/{item['id']}")
    assert response.status_code == 200
    assert response.json() == item


def test_update_item(client):
    item = create(client)
    response = client.put(
        f"{ITEMS_URL}/{item['id']}",
        json={"name": "Laptop Pro", "price": 1299.99, "in_stock": False},
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Laptop Pro", "price": 1299.99, "in_stock": False}


def test_delete_item(client):
    item = create(client)
    assert client.delete(f"{ITEMS_URL}/{item['id']}").status_code == 204
    assert client.get(f"{ITEMS_URL}/{item['id']}").status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_item_returns_404(client, method):
    kwargs = {"json": {"name": "X", "price": 1}} if method == "put" else {}
    response = getattr(client, method)(f"{ITEMS_URL}/999", **kwargs)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item 999 not found"}


@pytest.mark.parametrize(
    "body",
    [
        {"name": "", "price": 10},  # empty name
        {"name": "Laptop", "price": 0},  # price must be > 0
        {"name": "Laptop"},  # missing price
    ],
)
def test_invalid_item_returns_422(client, body):
    assert client.post(ITEMS_URL, json=body).status_code == 422
