from fastapi_storages import FileSystemStorage
from io import BytesIO


class StorageRepository:
    def __init__(self) -> None:
        self.storage = FileSystemStorage(path="storage")

    def read_file(self, filename: str) -> BytesIO:
        return BytesIO(self.storage.open(filename).read())

