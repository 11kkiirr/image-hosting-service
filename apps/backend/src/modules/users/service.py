from core.logger import logger
from core.database import UnitOfWork
from .models import User, UserPermission
from .schemas import UserCreate, UserUpdate, Language


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: int) -> User | None:
        return await self.uow.users.get(user_id)

    async def get_or_create_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        referrer_id: int | None = None,
    ) -> User:
        existing = await self.get_user(user_id)
        if existing is not None:
            return existing
        return await self.create_user(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referrer_id=referrer_id,
        )

    async def create_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        referrer_id: int | None = None,
    ) -> User:
        try:
            user_data = UserCreate(
                id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                referrer_id=referrer_id,
            )
            user = await self.uow.users.create(**user_data.model_dump())
            await self.uow.users.permissions.create(user_id=user.id)
            await self.uow.session.refresh(user, attribute_names=["permission"])
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = await self.uow.users.get(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")

        updates = data.model_dump(exclude_none=True)
        for key, value in updates.items():
            setattr(user, key, value)

        await self.uow.session.flush()
        await self.uow.session.refresh(user)
        return user

    async def set_language(self, user_id: int, lang: Language) -> User:
        return await self.update_user(user_id, UserUpdate(lang=lang))

    async def toggle_mailings(self, user_id: int) -> User:
        user = await self.uow.users.get(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")

        user.sand_mailings = not user.sand_mailings
        await self.uow.session.flush()
        await self.uow.session.refresh(user)
        return user

    async def get_referrals(self, user_id: int) -> list[User]:
        return await self.uow.users.get_referrals(user_id)

    async def count_referrals(self, user_id: int) -> int:
        return await self.uow.users.count_referrals(user_id)

    async def get_permission(self, user_id: int) -> UserPermission | None:
        return await self.uow.users.permissions.get_by_user_id(user_id)

    async def update_permission(
        self, user_id: int, **fields: bool
    ) -> UserPermission:
        perm = await self.uow.users.permissions.get_by_user_id(user_id)
        if perm is None:
            raise ValueError(f"Permissions for user {user_id} not found")

        valid_fields = {
            "is_superuser", "mailing", "resolve_disputes",
            "support", "users_list", "change_permissions", "stats",
        }
        for key, value in fields.items():
            if key not in valid_fields:
                raise ValueError(f"Unknown permission field: {key}")
            setattr(perm, key, value)

        await self.uow.session.flush()
        await self.uow.session.refresh(perm)
        return perm

    async def toggle_permission(
        self, user_id: int, field: str
    ) -> UserPermission:
        perm = await self.uow.users.permissions.get_by_user_id(user_id)
        if perm is None:
            raise ValueError(f"Permissions for user {user_id} not found")

        current = getattr(perm, field, None)
        if not isinstance(current, bool):
            raise ValueError(f"Unknown permission field: {field}")

        setattr(perm, field, not current)
        await self.uow.session.flush()
        await self.uow.session.refresh(perm)
        return perm
