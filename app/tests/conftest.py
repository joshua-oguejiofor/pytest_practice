from collections.abc import AsyncGenerator

import pytest  # noqa: F401
import pytest_asyncio
from database import get_db
from httpx import ASGITransport, AsyncClient
from main import app
from model import Base
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

"""
Assigning single responsiblity to each fixture: 
* test_engine: responsible for managing database engine( creating and closing.)
* setup_database: for creation and deletion of all tables
* db_session: for session used by each test function, it create a fresh session for each test-function, then perform cleanup after using the rollback
* override: overides the application get_db to the isolated test override_get_db
"""


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """This fixture is responsible for the creation and deletion of the database engine."""

    test_engine = create_async_engine(
        "sqlite+aiosqlite:///./testdb.db",
        echo=False
        )
    
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def setup_database(test_engine: AsyncEngine) -> AsyncGenerator[None, None]:
    """This fixture is responsible for creating all table in the database and deleting after test completes."""
    
    async with test_engine.begin() as engine:
        await engine.run_sync(Base.metadata.drop_all) # Drops any left-out table to get a fresh db state
        await engine.run_sync(Base.metadata.create_all)
        
        yield
    
    async with test_engine.begin() as engine:
        await engine.run_sync(Base.metadata.drop_all)

# This runs fresh for each test-function
@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine: AsyncEngine, setup_database: None) -> AsyncGenerator[AsyncSession, None]:
    
    async with test_engine.connect() as engine:
        transaction = await engine.begin()

        TestSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
            join_transaction_mode="create_savepoint",
            
        )
        async with TestSessionLocal() as session:
            try: 
                yield session
            finally:
                """Closes at the end the session and also rollback the data in the database"""
                await session.close()
                if transaction.is_active:
                    await transaction.rollback()
            


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[None, None]:
    """Provides an HTTPX AsyncClient with overridden database dependencies."""
    
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), 
            base_url="http://test",
            ) as asyc_client:
    
            yield asyc_client
    
    finally:
        app.dependency_overrides.clear()







# from collections.abc import AsyncGenerator

# import pytest
# import pytest_asyncio
# from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import (
#     AsyncEngine,
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine,
# )

# from app.database import get_db
# from app.main import app
# from app.model import Base

# # --- Use pytest_asyncio.fixture for ASYNC fixtures ---

# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
#     engine = create_async_engine(
#         "sqlite+aiosqlite:///./testdb.db",
#         echo=False
#     )
#     yield engine
#     await engine.dispose()  # Note: await engine.dispose() for async engine!


# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def setup_database(test_engine: AsyncEngine) -> AsyncGenerator[None, None]:
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
        
#     yield
    
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest_asyncio.fixture(scope="function")
# async def db_session(test_engine: AsyncEngine, setup_database: None) -> AsyncGenerator[AsyncSession, None]:
#     async with test_engine.connect() as conn:
#         transaction = await conn.begin()

#         TestSessionLocal = async_sessionmaker(
#             bind=conn,
#             class_=AsyncSession,
#             expire_on_commit=False,
#             autoflush=False,
#             autocommit=False,
#             join_transaction_mode="create_savepoint",
#         )
#         async with TestSessionLocal() as session:
#             try: 
#                 yield session
#             finally:
#                 await session.close()  # Note: Added missing () here!
#                 if transaction.is_active:
#                     await transaction.rollback()


# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def override(db_session: AsyncSession) -> AsyncGenerator[None, None]:
#     async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
#         yield db_session

#     app.dependency_overrides[get_db] = override_get_db
#     yield 
#     app.dependency_overrides.clear()


# # --- Use standard @pytest.fixture for SYNCHRONOUS fixtures ---

# @pytest.fixture(scope="function")
# def client():
#     with TestClient(app) as test_client:
#         yield test_client







