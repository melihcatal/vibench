from dataclasses import dataclass
from typing import Optional

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
    public_url: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600

@dataclass
class PresignedDownloadResponse:
    signed_url: str

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str

@dataclass
class ObjectMetadataResponse:
    object_name: str
    size: int
    content_type: Optional[str]
    etag: Optional[str]
    updated: Optional[str]

@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    delimiter: Optional[str] = None

@dataclass
class ListPrefixResponse:
    objects: list[str]
    prefixes: list[str]
