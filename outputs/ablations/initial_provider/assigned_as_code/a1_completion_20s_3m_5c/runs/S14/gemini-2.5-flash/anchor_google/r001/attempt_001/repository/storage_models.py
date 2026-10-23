from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class UploadObjectRequest:
    object_name: str
    data: bytes
    content_type: Optional[str] = "application/octet-stream"

@dataclass
class UploadObjectResponse:
    object_name: str

@dataclass
class PresignedDownloadRequest:
    object_name: str
    expiration_seconds: int = 3600 # 1 hour

@dataclass
class PresignedDownloadResponse:
    url: str

@dataclass
class ObjectMetadataRequest:
    object_name: str

@dataclass
class ObjectMetadataResponse:
    object_name: str
    size: int
    content_type: Optional[str]
    etag: Optional[str]
    updated: Optional[str]
    metadata: Optional[Dict[str, str]] = field(default_factory=dict)

@dataclass
class ListPrefixRequest:
    prefix: str = ""
    delimiter: Optional[str] = None

@dataclass
class ListPrefixResponse:
    objects: list[str] = field(default_factory=list)
    prefixes: list[str] = field(default_factory=list)
