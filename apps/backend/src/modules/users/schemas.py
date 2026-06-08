from enum import Enum
from uuid import UUID

from core.database.base import BaseSchema, TimestampReadSchema


class Language(str, Enum):
    EN = "EN"
    UA = "UA"
    RU = "RU"


class UserPermissionRead(TimestampReadSchema):
    id: UUID
    user_id: int
    is_superuser: bool
    mailing: bool
    resolve_disputes: bool
    support: bool
    users_list: bool
    change_permissions: bool
    stats: bool


class UserRead(TimestampReadSchema):
    id: int
    username: str | None
    first_name: str
    last_name: str | None
    sand_mailings: bool
    lang: Language
    referrer_id: int | None
    permission: UserPermissionRead | None = None


class UserCreate(BaseSchema):
    id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
    sand_mailings: bool = True
    lang: Language = Language.EN
    referrer_id: int | None = None


class UserUpdate(BaseSchema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    sand_mailings: bool | None = None
    lang: Language | None = None
