from typing import TypedDict, List

class ObjectMetadata(TypedDict):
    name: str
    size: int
    last_modified: str
    etag: str
    storage_class: str

class UploadResult(TypedDict):
    key: str
    etag: str

class ListResult(TypedDict):
    keys: List[str]
    continuation_token: str | None
