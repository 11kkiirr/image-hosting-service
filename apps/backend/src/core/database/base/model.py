import uuid
from datetime import datetime

from sqlalchemy import Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """DeclarativeBase для всех моделей проекта"""


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class BaseModel(TimestampMixin, Base):
    """Абстрактная модель с UUID PK и таймстемпами"""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )
