from sqlmodel.ext.asyncio.session import AsyncEngine,AsyncSession
from sqlmodel import create_engine
from src.config import settings
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager # For async context
DATABASE_URL=settings.database_url

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))

async_session_factory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit() # Commit transaction if no exceptions
        except Exception:
            await session.rollback() # Rollback on exception
            raise
        finally:
            await session.close() # Ensure session is closed
