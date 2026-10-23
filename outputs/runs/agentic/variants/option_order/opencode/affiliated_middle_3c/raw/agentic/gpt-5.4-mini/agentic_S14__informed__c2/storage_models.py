from dataclasses import dataclass, field
from typing import Any


def normalize_metadata(value: Any) -> dict:
    if not value:
        return {}
    return {str(k): '' if v is None else str(v) for k, v in dict(value).items()}


@dataclass
class UploadObjectRequest:
    object_name: str
    body: Any
    content_type: str | None = None
    metadata: dict | None = None


@dataclass
class UploadObjectResponse:
    bucket_name: str
    object_name: str
    etag: str | None = None
    generation: str | int | None = None


@dataclass
class PresignedDownloadRequest:
    object_name: str
    expires_in: int = 3600


@dataclass
class PresignedDownloadResponse:
    bucket_name: str
    object_name: str
    url: str
    expires_in: int


@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_name: str
    size: int | None = None
    content_type: str | None = None
    metadata: dict = field(default_factory=dict)
    etag: str | None = None
    updated: Any = None


@dataclass
class ListedObject:
    name: str
    size: int | None = None
    content_type: str | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: str
    objects: list[ListedObject] = field(default_factory=list)
