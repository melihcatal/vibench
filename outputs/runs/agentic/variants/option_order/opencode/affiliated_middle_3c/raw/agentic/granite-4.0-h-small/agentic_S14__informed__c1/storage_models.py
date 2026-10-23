from typing import TypedDict, Optional


class ObjectMetadata(TypedDict):
    Bucket: str
    Key: str
    Size: Optional[int]
    ETag: Optional[str]
    LastModified: Optional[str]
    StorageClass: Optional[str]
    ContentType: Optional[str]
    ContentDisposition: Optional[str]
    Metadata: Optional[dict]


class UploadResult(TypedDict):
    Bucket: str
    Key: str
    VersionId: Optional[str]


class PresignedUrlResult(TypedDict):
    url: str


class ListResult(TypedDict):
    Key: str
    LastModified: str
    ETag: str
    Size: int
    StorageClass: str
