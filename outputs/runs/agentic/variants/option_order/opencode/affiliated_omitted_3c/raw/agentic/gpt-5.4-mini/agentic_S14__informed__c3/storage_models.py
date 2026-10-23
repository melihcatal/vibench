from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: bytes
    content_type: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expires_in_seconds: int = 3600


@dataclass
class PresignedUrlResponse:
    bucket: str
    key: str
    url: str
    expires_in_seconds: int


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None


@dataclass
class ListedObject:
    key: str
    size: int
    last_modified: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[ListedObject]
    is_truncated: bool
    next_continuation_token: Optional[str] = None


def normalize_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_metadata(value: Any) -> dict[str, str]:
    return {str(k): str(v) for k, v in (value or {}).items()}


def normalize_etag(value: Any) -> Optional[str]:
    return None if value is None else str(value).strip('"')


def normalize_version_id(value: Any) -> Optional[str]:
    return None if value is None else str(value)
