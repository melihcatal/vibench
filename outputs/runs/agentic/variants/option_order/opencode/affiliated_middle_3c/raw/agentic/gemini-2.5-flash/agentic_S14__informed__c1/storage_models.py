from typing import Optional, Dict, Any
from dataclasses import dataclass


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
    content_type: Optional[str] = None
    e_tag: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600


@dataclass
class PresignedDownloadResponse:
    url: str


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
    e_tag: Optional[str] = None
    metadata: Dict[str, Any] = {}


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    delimiter: Optional[str] = None


@dataclass
class ListedObject:
    object_name: str
    size: int
    updated: Optional[str] = None


@dataclass
class ListPrefixResponse:
    objects: list[ListedObject]
    prefixes: list[str] = []
