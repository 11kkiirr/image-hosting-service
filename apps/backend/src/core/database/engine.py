from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.engine import URL


from core.database.base import Base
from core import config

database_url = URL.create(
    drivername=f"{config.DATABASE_SYSTEM.get_secret_value()}+{config.DATABASE_DRIVER.get_secret_value()}",
    database=config.DATABASE_NAME.get_secret_value(),
    username=config.DATABASE_USER.get_secret_value(),
    password=config.DATABASE_PASSWORD.get_secret_value(),
    port=int(config.DATABASE_PORT.get_secret_value()),
    host=config.DATABASE_HOST.get_secret_value(),
)


engine = create_async_engine(database_url, echo=False)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
