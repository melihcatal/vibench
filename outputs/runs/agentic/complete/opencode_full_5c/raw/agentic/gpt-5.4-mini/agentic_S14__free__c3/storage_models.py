from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_bucket_name(value: str) -> str:
    return value.strip()


def normalize_object_key(value: str) -> str:
    return value.lstrip("/")


@dataclass
class UploadObjectRequest:
    bucket: str
    key: str
    body: Any
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadObjectResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    keys: List[str]


@dataclass
class PresignedDownloadResponse:
    bucket: str
    key: str
    url: str
    expires_in: int
