from pydantic import BaseModel, ConfigDict, ValidationInfo, computed_field
import os

from app.schemas import BaseSearchSchema

domain = os.getenv("DOMAIN", "localhost")


class LessonSchema(BaseModel):
    id: int
    title: str
    level: int
    description: str | None = None

    @computed_field
    def audio_url(self) -> str:
        return "https://" + domain + "/api/lesson/" + str(self.id)

    model_config = ConfigDict(from_attributes=True)


class LessonShortSchema(BaseModel):
    id: int
    title: str
    level: int
    description: str | None = None

    @computed_field
    def audio_url(self) -> str:
        return "https://" + domain + "/api/lesson/" + str(self.id)

    model_config = ConfigDict(from_attributes=True)


class LessonSearchSchema(BaseSearchSchema):
    pass
