import databases
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession
)

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
