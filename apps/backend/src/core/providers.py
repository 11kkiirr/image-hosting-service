from typing import Callable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dishka import Provider, Scope, provide
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from .config import Config, config
from .database.engine import session_maker
from .database.uow import UnitOfWork


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return config

    @provide(scope=Scope.APP)
    def get_bot(self) -> Bot:
        return Bot(
            token=config.BOT_TOKEN.get_secret_value(),
            default=DefaultBotProperties(parse_mode="HTML"),
        )

    @provide(scope=Scope.APP)
    def get_sessionmaker(self) -> Callable[[], AsyncSession]:
        return session_maker

    @provide(scope=Scope.REQUEST)
    async def get_uow(self) -> AsyncIterator[UnitOfWork]:
        uow = UnitOfWork(session_maker)
        async with uow:
            yield uow
