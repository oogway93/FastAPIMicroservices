import jwt
from typing import Any
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, session: AsyncSession) -> None:
    response: Response = await client.post(
        "/auth/register",
        json={
            "username": "qwerty",
            "email": "example@gmail.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert len(data["user_id"]) != 0
    assert len(data["profile_id"]) != 0


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, session: AsyncSession) -> None:
    response: Response = await client.post(
        "/auth/register",
        json={
            "username": "qwerty",
            "email": "example@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201

    response: Response = await client.post(
        "/auth/login", json={"username": "qwerty", "password": "password123"}
    )

    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert "access_token" in data
    assert "token_type" in data

    assert data["token_type"] == "bearer"
    encodedToken = jwt.decode_complete(
        data["access_token"], key="secret_key", algorithms=["HS256"]
    )
    assert encodedToken["payload"]["sub"] == "qwerty"


@pytest.mark.asyncio
async def test_protected_endpoint(client: AsyncClient, session: AsyncSession) -> None:
    response: Response = await client.post(
        "/auth/register",
        json={
            "username": "qwerty",
            "email": "example@gmail.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    response: Response = await client.post(
        "/auth/login", json={"username": "qwerty", "password": "password123"}
    )
    token: str = response.json()["access_token"]

    response: Response = await client.get(
        "/auth/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data: dict[str, Any] = response.json()["current user info"]
    assert data["email"] == "example@gmail.com"
    assert data["username"] == "qwerty"
