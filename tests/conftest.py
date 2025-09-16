import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from app.database import Base, get_db
from app.main import app
from asgi_lifespan import LifespanManager
import os
from app.models import *

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Async Engine & Session für Test-DB
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency override
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        def sync_inspect(connection):
            insp = inspect(connection)
            print("Tables in test DB:", insp.get_table_names())
        await conn.run_sync(sync_inspect)

    # Insert Test-User
    async with TestingSessionLocal() as session:
        test_user = User(id=1, username="Test User")
        session.add(test_user)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# AsyncClient Fixture mit LifespanManager
@pytest_asyncio.fixture
async def async_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
