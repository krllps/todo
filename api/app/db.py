from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

DATABASE_URL = settings.PG_DB_URL
engine = create_async_engine(DATABASE_URL, echo=True, future=True)  # echo=True flashes SQL queries to logs
Base = declarative_base()


async def get_db() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()
