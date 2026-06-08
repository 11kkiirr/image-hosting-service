from dishka import Provider, Scope, provide

from core.database.uow import UnitOfWork
from .service import UserService


class UsersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(self, uow: UnitOfWork) -> UserService:
        return UserService(uow)
