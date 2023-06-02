import pytest, httpx, asyncio
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_read_item():
    response = await client.get("/api/todo")
    assert response.status_code == 200
