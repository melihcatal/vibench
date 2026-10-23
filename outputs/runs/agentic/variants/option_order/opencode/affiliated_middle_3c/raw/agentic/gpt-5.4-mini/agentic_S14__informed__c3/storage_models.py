from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class UploadObjectRequest:
    bucket: str
    key: str
    content_type: str | None = None


@dataclass
class UploadObjectResponse:
    bucket: str
    key: str
    etag: str | None = None
    version_id: str | None = None


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    size: int | None = None
    etag: str | None = None
    content_type: str | None = None
    last_modified: str | None = None
    extra: dict[str, Any] | None = None


def normalize_dict(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if hasattr(value, "items"):
        return dict(value)
    return value


def to_dict(instance):
    return asdict(instance)
