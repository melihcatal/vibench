from typing import Optional, Dict, List, Union, BinaryIO
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UploadRequest:
    object_key: str
    content: Union[str, bytes, BinaryIO]
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclass
class UploadResponse:
    object_key: str
    bucket_name: str
    success: bool
    etag: Optional[str] = None
    error: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    object_key: str
    expiry_minutes: int = 15

@dataclass
class PresignedDownloadResponse:
    download_url: str
    object_key: str
    expiry_minutes: int
    success: bool
    error: Optional[str] = None

@dataclass
class ObjectMetadataRequest:
    object_key: str

@dataclass
class ObjectMetadataResponse:
    object_key: str
    metadata: Dict[str, str]
    content_type: Optional[str]
    content_length: int
    last_modified: Optional[datetime]
    etag: Optional[str]
    success: bool
    error: Optional[str] = None

@dataclass
class ObjectSummary:
    object_key: str
    size: int
    last_modified: datetime
    etag: str

@dataclass
class ListPrefixRequest:
    prefix: str
    max_keys: int = 1000

@dataclass
class ListPrefixResponse:
    prefix: str
    objects: List[ObjectSummary]
    success: bool
    error: Optional[str] = None