from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ObjectMetadata:
    name: str
    size: int
    content_type: Optional[str]
    time_created: datetime
    updated: datetime
    md5_hash: Optional[str]
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadRequest:
    object_name: str
    data: bytes
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    object_name: str
    public_url: Optional[str] = None
    size: Optional[int] = None


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_at: datetime


@dataclass
class ListPrefixResponse:
    objects: List[ObjectMetadata]
    prefixes: List[str]