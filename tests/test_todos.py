"""API tests for todo operations."""

import os

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

import app.database as db_module
from app.database import init_db
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def setup_db(tmp_path):
    """Create a fresh database for each test."""
    test_db_path = str(tmp_path / "test.db")
    db_module.DATABASE_PATH = test_db_path
    await init_db()
    yield
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest_asyncio.fixture
async def client():
    """Provide an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# --- GET /api/todos ---


async def test_list_todos_empty(client):
    """Empty list returns 200 with empty array."""
    res = await client.get("/api/todos/")
    assert res.status_code == 200
    assert res.json() == []


async def test_list_todos_with_items(client):
    """List returns all created todos."""
    await client.post("/api/todos/", json={"title": "First"})
    await client.post("/api/todos/", json={"title": "Second"})
    res = await client.get("/api/todos/")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2


# --- POST /api/todos ---


async def test_create_todo_success(client):
    """Create a todo with valid title."""
    res = await client.post("/api/todos/", json={"title": "Buy milk"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


async def test_create_todo_empty_title(client):
    """Reject empty title with 422."""
    res = await client.post("/api/todos/", json={"title": ""})
    assert res.status_code == 422


async def test_create_todo_whitespace_title(client):
    """Reject whitespace-only title with 422."""
    res = await client.post("/api/todos/", json={"title": "   "})
    assert res.status_code == 422


async def test_create_todo_strips_whitespace(client):
    """Title is stripped of leading/trailing whitespace."""
    res = await client.post("/api/todos/", json={"title": "  Buy milk  "})
    assert res.status_code == 201
    assert res.json()["title"] == "Buy milk"


# --- PATCH /api/todos/{id} ---


async def test_toggle_todo_complete(client):
    """Toggle a todo to completed."""
    create_res = await client.post("/api/todos/", json={"title": "Test"})
    todo_id = create_res.json()["id"]
    res = await client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert res.status_code == 200
    assert res.json()["completed"] is True


async def test_toggle_todo_incomplete(client):
    """Toggle a completed todo back to incomplete."""
    create_res = await client.post("/api/todos/", json={"title": "Test"})
    todo_id = create_res.json()["id"]
    await client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    res = await client.patch(f"/api/todos/{todo_id}", json={"completed": False})
    assert res.status_code == 200
    assert res.json()["completed"] is False


async def test_update_todo_title(client):
    """Update a todo's title."""
    create_res = await client.post("/api/todos/", json={"title": "Old"})
    todo_id = create_res.json()["id"]
    res = await client.patch(f"/api/todos/{todo_id}", json={"title": "New"})
    assert res.status_code == 200
    assert res.json()["title"] == "New"


async def test_update_todo_empty_title(client):
    """Reject empty title update with 422."""
    create_res = await client.post("/api/todos/", json={"title": "Test"})
    todo_id = create_res.json()["id"]
    res = await client.patch(f"/api/todos/{todo_id}", json={"title": ""})
    assert res.status_code == 422


async def test_update_todo_not_found(client):
    """Return 404 for non-existent todo."""
    res = await client.patch("/api/todos/9999", json={"completed": True})
    assert res.status_code == 404


async def test_update_todo_no_fields(client):
    """Reject update with no fields."""
    create_res = await client.post("/api/todos/", json={"title": "Test"})
    todo_id = create_res.json()["id"]
    res = await client.patch(f"/api/todos/{todo_id}", json={})
    assert res.status_code == 400


# --- DELETE /api/todos/{id} ---


async def test_delete_todo_success(client):
    """Delete an existing todo."""
    create_res = await client.post("/api/todos/", json={"title": "Test"})
    todo_id = create_res.json()["id"]
    res = await client.delete(f"/api/todos/{todo_id}")
    assert res.status_code == 204

    list_res = await client.get("/api/todos/")
    assert len(list_res.json()) == 0


async def test_delete_todo_not_found(client):
    """Return 404 for non-existent todo."""
    res = await client.delete("/api/todos/9999")
    assert res.status_code == 404
