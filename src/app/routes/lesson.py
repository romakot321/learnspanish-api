from fastapi import APIRouter, Depends

from fastapi.responses import Response

from app.schemas.lesson import (
    LessonSearchSchema,
    LessonShortSchema,
)
from app.services.lesson import LessonService
from . import validate_api_token

router = APIRouter(prefix="/api/lesson", tags=["Lesson"])


@router.get(
    "/{lesson_id}", response_class=Response, dependencies=[Depends(validate_api_token)]
)
async def get_lesson_file(lesson_id: int, service: LessonService = Depends()):
    buffer = await service.get_file(lesson_id)
    return Response(content=buffer.getvalue(), media_type="audio/wav")


@router.get(
    "",
    response_model=list[LessonShortSchema],
    dependencies=[Depends(validate_api_token)],
)
async def get_lessons_list(
    schema: LessonSearchSchema = Depends(), service: LessonService = Depends()
):
    return await service.get_list(schema)
