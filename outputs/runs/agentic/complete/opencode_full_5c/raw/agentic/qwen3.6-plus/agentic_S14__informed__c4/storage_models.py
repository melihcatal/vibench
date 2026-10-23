from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class UploadRequest:
    bucket: str
    key: str
    data: bytes
    content_type: str = "application/octet-stream"
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class UploadResponse:
    success: bool
    object_key: str
    bucket: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expiration_seconds: int = 3600
    http_method: str = "GET"
    response_content_disposition: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    success: bool
    url: Optional[str] = None
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class MetadataRequest:
    bucket: str
    key: str


@dataclass
class MetadataResponse:
    success: bool
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str
    delimiter: str = ""
    max_keys: int = 1000
    continuation_token: Optional[str] = None


@dataclass
class ObjectSummary:
    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str
    content_type: Optional[str] = None


@dataclass
class ListPrefixResponse:
    success: bool
    objects: List[ObjectSummary] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    error: Optional[str] = None
