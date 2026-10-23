from typing import TypedDict, Any


class ObjectMetadata(TypedDict):
    LastModified: str
    Size: int
    ETag: str
    StorageClass: str
    Metadata: dict[str, str]


class UploadResult(TypedDict):
    status: str
    object_key: str
    version_id: str | None = None
    etag: str | None = None


class DownloadResult(TypedDict):
    url: str
    expires_at: int


class ListObjectSummary(TypedDict):
    Key: str
    LastModified: str
    Size: int
    StorageClass: str


class PresignParams(TypedDict):
    bucket: str
    key: str
    expiry_seconds: int
