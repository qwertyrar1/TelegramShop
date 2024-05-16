from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

