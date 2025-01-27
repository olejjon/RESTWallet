import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Wallet

# Переопределение настроек базы данных для тестов
TEST_DATABASE_URL = "postgresql+asyncpg://user:123@localhost:5432/test_walletdb"

@pytest.fixture
def client():
    return TestClient(app)

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as connection:
        AsyncSessionLocal = sessionmaker(
            bind=connection, class_=AsyncSession, expire_on_commit=False
        )
        async with AsyncSessionLocal() as session:
            yield session

@pytest.mark.asyncio
async def test_create_wallet(client, db_session):
    wallet_data = {"uuid": "wallet_1", "balance": 100.0}
    response = client.post("/api/v1/wallets", json=wallet_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Wallet created successfully"