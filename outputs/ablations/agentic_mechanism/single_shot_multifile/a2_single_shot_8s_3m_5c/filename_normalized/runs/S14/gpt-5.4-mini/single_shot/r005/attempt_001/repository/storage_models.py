from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def coerce_bytes(body: Any) -> bytes:
    if isinstance(body, bytes):
        return body
    if isinstance(body, str):
        return body.encode('utf-8')
    if hasattr(body, 'read'):
        data = body.read()
        return data if isinstance(data, bytes) else str(data).encode('utf-8')
    raise TypeError('unsupported body type')


def normalize_s3_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    return {str(k): '' if v is None else str(v) for k, v in (metadata or {}).items()}


def normalize_s3_object(obj: dict[str, Any]) -> 'ListedObject':
    return ListedObject(
        key=str(obj.get('Key', '')),
        size=int(obj.get('Size', 0)),
        last_modified=obj.get('LastModified'),
        etag=obj.get('ETag'),
        storage_class=obj.get('StorageClass'),
    )


@dataclass(slots=True)
class UploadRequest:
    bucket: str | None
    key: str
    body: Any
    content_type: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    server_side_encryption: str | None = None


@dataclass(slots=True)
class UploadResponse:
    bucket: str
    key: str
    content_length: int | None = None
    etag: str | None = None


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str | None
    key: str
    expires_in: int = 3600


@dataclass(slots=True)
class PresignedDownloadResponse:
    url: str
    expires_in: int


@dataclass(slots=True)
class ObjectMetadataRequest:
    bucket: str | None
    key: str


@dataclass(slots=True)
class ObjectMetadataResponse:
    bucket: str
    key: str
    content_length: int | None = None
    content_type: str | None = None
    etag: str | None = None
    last_modified: datetime | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int
    last_modified: Any = None
    etag: str | None = None
    storage_class: str | None = None


@dataclass(slots=True)
class ListPrefixRequest:
    bucket: str | None
    prefix: str | None = None


@dataclass(slots=True)
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: list[ListedObject] = field(default_factory=list)
