from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Base

ModelType = TypeVar("ModelType", bound=Base)
PKType = TypeVar("PKType")

class BaseRepository(Generic[ModelType, PKType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: PKType) -> ModelType | None:
        id_column = getattr(self.model, "id")
        result = await self.session.execute(
            select(self.model).filter(id_column == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_criteria(self, **kwargs: Any) -> ModelType | None:
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        result = await self.session.execute(select(self.model).filter(*filters))
        return result.scalar_one_or_none()
    
    async def get_all_by_criteria(self, **kwargs: Any) -> Sequence[ModelType]:
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        result = await self.session.execute(select(self.model).filter(*filters))
        return result.scalars().all()

    async def create(self, **kwargs: Any) -> ModelType:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: PKType) -> bool:
        obj = await self.get(id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.flush()
        return True
