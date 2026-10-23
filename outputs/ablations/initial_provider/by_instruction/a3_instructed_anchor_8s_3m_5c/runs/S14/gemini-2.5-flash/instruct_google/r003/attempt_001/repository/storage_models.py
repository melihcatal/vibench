import dataclasses
from typing import Optional

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None

@dataclasses.dataclass
class UploadObjectResponse:
    bucket_name: str
    object_name: str
    size: int
    self_link: str

@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int

@dataclasses.dataclass
class PresignedDownloadResponse:
    signed_url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    object_name: str
    size: int
    content_type: str
    etag: str
    updated: str

@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: Optional[str] = None
    max_results: Optional[int] = None

@dataclasses.dataclass
class ListPrefixResponse:
    object_names: list[str]
