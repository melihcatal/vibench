from typing import TypedDict, List


class ObjectMetadata(TypedDict):
    Key: str
    ETag: str
    Size: int
    LastModified: str
    StorageClass: str


class UploadResult(TypedDict):
    UploadId: str
    Key: str
    Bucket: str


class PresignParams(TypedDict):
    ExpiresIn: int


class ListResult(TypedDict):
    CommonPrefixes: List[str]
    Contents: List[ObjectMetadata]
