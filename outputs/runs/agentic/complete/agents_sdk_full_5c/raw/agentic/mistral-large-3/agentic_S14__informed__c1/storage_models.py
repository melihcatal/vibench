from typing import Dict, Optional, TypedDict
from dataclasses import dataclass


@dataclass
class ObjectMetadata:
    key: str
    size: int
    etag: str
    last_modified: str
    storage_class: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class UploadRequest(TypedDict):
    key: str
    body: bytes
    content_type: Optional[str]
    metadata: Optional[Dict[str, str]]


class UploadResponse(TypedDict):
    key: str
    etag: str
    version_id: Optional[str]


class PresignedDownloadResponse(TypedDict):
    url: str
    expires_in: int