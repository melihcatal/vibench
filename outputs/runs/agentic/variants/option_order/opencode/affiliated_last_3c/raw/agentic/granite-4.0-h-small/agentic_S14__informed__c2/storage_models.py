from typing import TypedDict, List, Optional


class ObjectMetadata(TypedDict):
    ETag: str
    Size: int
    LastModified: str
    ContentType: str
    Metadata: Optional[dict]


class ListObject(TypedDict):
    Key: str
    LastModified: str
    ETag: str
    Size: int
    StorageClass: str
    ContentType: str


class UploadResult(TypedDict):
    Key: str
    Location: str


class PresignParams(TypedDict):
    URL: str
    Expiration: int
