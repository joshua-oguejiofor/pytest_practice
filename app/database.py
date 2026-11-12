from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

db_url = "sqlite+aiosqlite:///./pytest.db"

engine = create_async_engine(
    url=db_url,
    echo=False,
    max_overflow=30,
    pool_size=20,
    pool_pre_ping = True,
    pool_recycle = 3600,
    )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False, 
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try: 
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        