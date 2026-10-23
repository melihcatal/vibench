# [HELPER] storage_models.py

from typing import TypedDict, Optional


class ObjectMetadata(TypedDict):
    Key: str
    Size: int
    ETag: str
    LastModified: str
    Metadata: Optional[dict]


class UploadResult(TypedDict):
    VersionId: Optional[str]
    ETag: Optional[str]


class ListResult(TypedDict):
    Key: str
    Size: int
    LastModified: str
    StorageClass: str
