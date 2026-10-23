from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: Union[bytes, BinaryIO]
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: str
    version_id: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600


@dataclass
class PresignedDownloadResponse:
    url: str


@dataclass
class ObjectMetadataRequest:
    bucket: str
    key: str


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    content_type: Optional[str]
    content_length: int
    etag: str
    last_modified: str
    metadata: Dict[str, str]
    version_id: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: Optional[str] = None
    max_keys: int = 1000


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: Optional[str]
    objects: list[dict]
    is_truncated: bool
    next_continuation_token: Optional[str] = None
