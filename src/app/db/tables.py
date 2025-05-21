import datetime as dt
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType

from sqlalchemy import text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as column

from sqlalchemy_service import Base
from sqlalchemy_service.base_db.base import ServiceEngine

sql_utcnow = text("(now() at time zone 'utc')")

engine = ServiceEngine()
storage = FileSystemStorage(path="storage")


class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        letters = ["_" + i.lower() if i.isupper() else i for i in cls.__name__]
        return "".join(letters).lstrip("_") + "s"

    id: M[int] = column(primary_key=True, index=True)
    created_at: M[dt.datetime] = column(server_default=sql_utcnow)
    updated_at: M[dt.datetime | None] = column(nullable=True, onupdate=sql_utcnow)


class Lesson(BaseMixin, Base):
    title: M[str]
    level: M[int] = column(doc="Глава")
    file: M[FileType] = column(type_=FileType(storage=storage), nullable=False)

