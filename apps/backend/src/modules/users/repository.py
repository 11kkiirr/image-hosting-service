from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.base.repository import BaseRepository
from .models import User, UserPermission


class UserPermissionRepository(BaseRepository[UserPermission, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserPermission, session)

    async def get_by_user_id(self, user_id: int) -> UserPermission | None:
        result = await self.session.execute(
            select(UserPermission).filter(UserPermission.user_id == user_id)
        )
        return result.scalar_one_or_none()


class UserRepository(BaseRepository[User, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    @property
    def permissions(self) -> UserPermissionRepository:
        return UserPermissionRepository(self.session)

    async def get_referrals(self, user_id: int) -> list[User]:
        result = await self.session.execute(
            select(User).filter(User.referrer_id == user_id)
        )
        return list(result.scalars().all())

    async def count_referrals(self, user_id: int) -> int:
        from sqlalchemy import func

        result = await self.session.execute(
            select(func.count()).select_from(User).filter(User.referrer_id == user_id)
        )
        return result.scalar_one()
