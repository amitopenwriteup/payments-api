import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_payment_success(async_client: AsyncClient):
    response = await async_client.post(
        "/payments/",
        json={"amount": 50.0, "currency": "USD", "description": "Test payment"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["amount"] == 50.0


@pytest.mark.asyncio
async def test_create_payment_negative_amount(async_client: AsyncClient):
    response = await async_client.post(
        "/payments/",
        json={"amount": -10.0},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_payment(async_client: AsyncClient):
    response = await async_client.get("/payments/pay_abc123")
    assert response.status_code == 200
    assert response.json()["payment_id"] == "pay_abc123"


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
