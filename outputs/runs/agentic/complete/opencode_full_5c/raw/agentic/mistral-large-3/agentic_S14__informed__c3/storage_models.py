from typing import Dict, Optional, TypedDict
from datetime import datetime


class UploadRequest(TypedDict):
    bucket_name: str
    object_key: str
    body: bytes
    content_type: Optional[str]
    metadata: Optional[Dict[str, str]]


class UploadResponse(TypedDict):
    bucket: str
    key: str
    status: str


class PresignedDownloadRequest(TypedDict):
    bucket_name: str
    object_key: str
    expiration: int


class PresignedDownloadResponse(TypedDict):
    url: str


class ObjectMetadataRequest(TypedDict):
    bucket_name: str
    object_key: str


class ObjectMetadataResponse(TypedDict):
    ContentType: Optional[str]
    ContentLength: Optional[int]
    ETag: Optional[str]
    LastModified: Optional[datetime]
    Metadata: Optional[Dict[str, str]]


class ListPrefixRequest(TypedDict):
    bucket_name: str
    prefix: str
    max_keys: int


class ListPrefixObject(TypedDict):
    Key: str
    Size: int
    LastModified: datetime
    ETag: str


class ListPrefixResponse(TypedDict):
    objects: list[ListPrefixObject]
