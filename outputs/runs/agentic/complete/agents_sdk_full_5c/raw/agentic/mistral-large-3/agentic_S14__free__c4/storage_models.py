from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, BinaryIO

@dataclass
class UploadRequest:
    bucket_name: str
    object_key: str
    file_stream: BinaryIO
    content_type: str = "application/octet-stream"
    metadata: Dict[str, str] = None

@dataclass
class UploadResponse:
    bucket_name: str
    object_key: str
    success: bool
    etag: Optional[str] = None
    error: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expiry_minutes: int = 15

@dataclass
class PresignedDownloadResponse:
    bucket_name: str
    object_key: str
    presigned_url: Optional[str]
    success: bool
    error: Optional[str] = None

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str

@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_key: str
    success: bool
    metadata: Optional[Dict[str, str]] = None
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    error: Optional[str] = None

@dataclass
class ListedObject:
    object_key: str
    size: int
    last_modified: datetime
    etag: str

@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str

@dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: str
    objects: List[ListedObject]
    success: bool
    error: Optional[str] = None