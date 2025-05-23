from io import BytesIO
from fastapi import Depends, HTTPException

from app.repositories.lesson import LessonRepository
from app.repositories.storage import StorageRepository
from app.schemas.lesson import LessonSchema, LessonSearchSchema, LessonShortSchema


class LessonService:
    def __init__(
            self,
            lesson_repository: LessonRepository = Depends(LessonRepository.depend),
            storage_repository: StorageRepository = Depends()
    ):
        self.lesson_repository = lesson_repository
        self.storage_repository = storage_repository

    async def get(self, lesson_id: int) -> LessonSchema:
        model = await self.lesson_repository.get(lesson_id)
        return LessonSchema.model_validate(model)

    async def get_list(self, schema: LessonSearchSchema) -> list[LessonShortSchema]:
        models = await self.lesson_repository.list(**schema.model_dump(exclude_none=True))
        return [
            LessonShortSchema.model_validate(model)
            for model in models
        ]

    async def get_file(self, lesson_id: int) -> BytesIO:
        model = await self.lesson_repository.get(lesson_id)
        return BytesIO(model.file.open().read())

    async def get_preview(self, lesson_id: int) -> BytesIO:
        model = await self.lesson_repository.get(lesson_id)
        if model.preview is None:
            raise HTTPException(404)
        return BytesIO(model.preview.open().read())
