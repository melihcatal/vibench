from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StorageObject:
    name: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadRequest:
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    object_name: str
    object_id: str
    size: int
    upload_timestamp: datetime


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_at: datetime


@dataclass
class ListPrefixResponse:
    objects: List[StorageObject]
    next_marker: Optional[str] = None