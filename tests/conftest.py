import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from app.core.database import Base, get_db
from app.main import app
from asgi_lifespan import LifespanManager
from app.core.models import User

# --------------------------
# In-Memory SQLite URL
# --------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Async Engine & Session
engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency override
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# --------------------------
# Fixture: Initialize DB
# --------------------------
@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        def sync_inspect(connection):
            insp = inspect(connection)
            print("Tables in test DB:", insp.get_table_names())

        await conn.run_sync(sync_inspect)

    # Insert test user
    async with TestingSessionLocal() as session:
        test_user = User(id=1, username="Test User") # ToDo: Adjust this!
        session.add(test_user)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --------------------------
# Fixture: AsyncClient with Lifespan
# --------------------------
@pytest_asyncio.fixture
async def async_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
