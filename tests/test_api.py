"""Functional API tests with isolated in-memory storage for each test."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.task_service import TaskService, get_task_service


@pytest.fixture
def client():
    """Give each test its own store and remove the override afterward."""
    service = TaskService()
    app.dependency_overrides[get_task_service] = lambda: service
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "devops-task-platform", "version": "0.1.0"}


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_initial_list_is_empty(client: TestClient) -> None:
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client: TestClient) -> None:
    response = client.post("/api/v1/tasks", json={"title": " Deploy the API "})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Deploy the API",
        "description": None,
        "completed": False,
    }


def test_list_and_get_task(client: TestClient) -> None:
    payload = {"title": "Add tests", "description": "Use pytest", "completed": True}
    created = client.post("/api/v1/tasks", json=payload)
    assert created.status_code == 201

    listed = client.get("/api/v1/tasks")
    assert listed.status_code == 200
    assert listed.json() == [created.json()]

    fetched = client.get("/api/v1/tasks/1")
    assert fetched.status_code == 200
    assert fetched.json() == created.json()


def test_delete_task(client: TestClient) -> None:
    client.post("/api/v1/tasks", json={"title": "Remove me"})
    deleted = client.delete("/api/v1/tasks/1")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get("/api/v1/tasks").json() == []


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_missing_task_returns_404(client: TestClient) -> None:
    response = client.delete("/api/v1/tasks/999")
    assert response.status_code == 404


@pytest.mark.parametrize("title", ["", "    "])
def test_blank_title_returns_422(client: TestClient, title: str) -> None:
    response = client.post("/api/v1/tasks", json={"title": title})
    assert response.status_code == 422
    assert client.get("/api/v1/tasks").json() == []


def test_missing_title_returns_422(client: TestClient) -> None:
    response = client.post("/api/v1/tasks", json={"description": "no title"})
    assert response.status_code == 422


def test_negative_task_id_returns_422(client: TestClient) -> None:
    response = client.get("/api/v1/tasks/-1")
    assert response.status_code == 422


def test_extra_fields_rejected(client: TestClient) -> None:
    response = client.post("/api/v1/tasks", json={"title": "OK", "unknown": 123})
    assert response.status_code == 422
