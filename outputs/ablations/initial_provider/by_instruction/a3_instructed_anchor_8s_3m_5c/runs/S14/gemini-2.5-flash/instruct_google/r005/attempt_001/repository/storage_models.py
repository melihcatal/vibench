from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    data: bytes
    content_type: Optional[str] = None

@dataclass
class UploadObjectResponse:
    bucket_name: str
    object_name: str
    size: int
    md5_hash: Optional[str] = None
    crc32c_hash: Optional[str] = None
    media_link: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600  # Default to 1 hour

@dataclass
class PresignedDownloadResponse:
    presigned_url: str

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str

@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_name: str
    size: int
    content_type: Optional[str] = None
    md5_hash: Optional[str] = None
    crc32c_hash: Optional[str] = None
    etag: Optional[str] = None
    time_created: Optional[str] = None
    updated: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: Optional[str] = None
    max_results: Optional[int] = None

@dataclass
class ListPrefixResponse:
    objects: list[str]
    next_page_token: Optional[str] = None
