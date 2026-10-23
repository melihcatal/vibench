from dataclasses import dataclass
from typing import Optional, Dict, Union, BinaryIO


@dataclass
class UploadRequest:
    bucket_name: str
    object_name: str
    data: Union[bytes, BinaryIO]
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    bucket_name: str
    object_name: str
    public_url: str
    size_bytes: int
    etag: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_hours: int = 1


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_at: str


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclass
class ObjectMetadataResponse:
    name: str
    size_bytes: int
    content_type: str
    time_created: str
    updated: str
    metadata: Dict[str, str]
    etag: str
    generation: str
    metageneration: str


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str = ""
    delimiter: str = "/"


@dataclass
class ListPrefixResponse:
    objects: list[str]
    prefixes: list[str]
