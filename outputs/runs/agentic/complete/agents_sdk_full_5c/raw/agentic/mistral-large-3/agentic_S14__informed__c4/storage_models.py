from typing import Dict, Optional, TypedDict
from datetime import datetime


class ObjectMetadata(TypedDict):
    name: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str
    metadata: Dict[str, str]


class UploadRequest:
    def __init__(self, bucket: str, key: str, body: bytes, metadata: Optional[Dict[str, str]] = None):
        self.bucket = bucket
        self.key = key
        self.body = body
        self.metadata = metadata or {}


class PresignedDownloadResponse:
    def __init__(self, url: str, expires_in: int):
        self.url = url
        self.expires_in = expires_in


class ListPrefixResponse:
    def __init__(self, objects: list[ObjectMetadata], prefix: str, bucket: str):
        self.objects = objects
        self.prefix = prefix
        self.bucket = bucket