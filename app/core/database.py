from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

engine = create_async_engine(settings.database_url,echo=True)

new_session = async_sessionmaker(engine,expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session



