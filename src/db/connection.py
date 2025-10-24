from sqlmodel.ext.asyncio.session import AsyncEngine
from sqlmodel import create_engine
from src.config import settings

DATABASE_URL=settings.database_url

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))