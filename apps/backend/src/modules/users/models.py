from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, Boolean, ForeignKey, Enum as SqlEnum

from core.database.base.model import Base, TimestampMixin, BaseModel
from modules.users.schemas import Language

if TYPE_CHECKING:
    from modules.accounting.models import Wallet

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sand_mailings: Mapped[bool] = mapped_column(Boolean, default=True)
    lang: Mapped[Language] = mapped_column(
        SqlEnum(Language, name="user_language", native_enum=False, validate_strings=True),
        nullable=False,
        default=Language.EN,
    )
    
    referrer_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    referrer: Mapped[User | None] = relationship(
        "User",
        remote_side=[id],
        back_populates="referred_users",
        lazy="selectin",
    )
    referred_users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="referrer",
        lazy="selectin",
    )

    permission: Mapped["UserPermission"] = relationship(
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )
    
    wallets: Mapped[list["Wallet"]] = relationship(
        "Wallet",
        back_populates="user",
        lazy="selectin",
    )
    
class UserPermission(BaseModel):
    __tablename__ = "user_permissions"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    mailing: Mapped[bool] = mapped_column(Boolean, default=False)
    resolve_disputes: Mapped[bool] = mapped_column(Boolean, default=False)
    support: Mapped[bool] = mapped_column(Boolean, default=False)
    users_list: Mapped[bool] = mapped_column(Boolean, default=False)
    change_permissions: Mapped[bool] = mapped_column(Boolean, default=False)
    stats: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped["User"] = relationship(
        back_populates="permission",
        lazy="selectin",
    )
