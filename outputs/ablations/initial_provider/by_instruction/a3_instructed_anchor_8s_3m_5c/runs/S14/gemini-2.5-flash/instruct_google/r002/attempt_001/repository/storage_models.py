from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class UploadObjectRequest:
    bucket_name: str
    destination_blob_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None

@dataclass
class UploadObjectResponse:
    bucket_name: str
    blob_name: str
    public_url: Optional[str] = None
    e_tag: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    blob_name: str
    expiration_seconds: int = 3600

@dataclass
class PresignedDownloadResponse:
    signed_url: str

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    blob_name: str

@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    blob_name: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    updated: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: Optional[str] = None
    max_results: Optional[int] = None

@dataclass
class ListPrefixResponse:
    blob_names: list[str]
