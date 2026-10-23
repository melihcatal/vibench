from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class UploadRequest:
    bucket_name: str
    object_key: str
    data: bytes
    content_type: str = "application/octet-stream"
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    key: str
    etag: str


@dataclass
class PresignedDownloadResponse:
    url: str
    expiry_time: datetime


@dataclass
class ObjectMetadataResponse:
    metadata: Dict[str, str]


@dataclass
class PrefixObject:
    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str


@dataclass
class ListPrefixResponse:
    objects: List[PrefixObject]
