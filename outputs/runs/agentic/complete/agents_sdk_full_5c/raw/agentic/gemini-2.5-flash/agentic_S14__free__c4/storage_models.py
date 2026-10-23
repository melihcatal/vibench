from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ObjectUploadRequest:
    bucket_name: str
    object_key: str
    file_path: Optional[str] = None
    data_bytes: Optional[bytes] = None
    content_type: Optional[str] = None

@dataclass
class ObjectUploadResponse:
    success: bool
    message: str
    etag: Optional[str] = None
    version_id: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expiration_seconds: int = 3600 # 1 hour default

@dataclass
class PresignedDownloadResponse:
    success: bool
    message: str
    presigned_url: Optional[str] = None

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str

@dataclass
class ObjectMetadataResponse:
    success: bool
    message: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ListObjectsRequest:
    bucket_name: str
    prefix: str = ""
    max_keys: int = 1000

@dataclass
class ListObjectsResponse:
    success: bool
    message: str
    object_keys: Optional[list[str]] = None
    common_prefixes: Optional[list[str]] = None
