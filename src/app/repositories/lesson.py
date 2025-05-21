from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_service import BaseService as BaseRepository

from app.db.tables import Lesson, engine


class LessonRepository[Table: Lesson, int](BaseRepository):
    base_table = Lesson
    engine = engine
    session: AsyncSession
    response: Response

    async def list(self, page=None, count=None) -> list[Lesson]:
        return list(await self._get_list(page=page, count=count))

    async def get(self, model_id: int) -> Lesson:
        return await self._get_one(
            id=model_id,
            select_in_load=[Lesson.items]
        )

    async def count(self):
        return await self._count()

