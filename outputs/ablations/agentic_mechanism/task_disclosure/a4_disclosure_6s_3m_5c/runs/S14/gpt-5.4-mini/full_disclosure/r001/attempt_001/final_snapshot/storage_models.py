from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
from urllib.parse import quote, urlparse


def _normalize_datetime(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return value
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            return value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    return value


def _normalize_etag(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    return text


def _normalize_storage_key(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    return value.lstrip("/")


def normalize_object_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(metadata)
    for key in ("created_at", "updated_at", "last_modified", "expires_at"):
        if key in normalized:
            normalized[key] = _normalize_datetime(normalized[key])
    for key in ("etag", "e_tag", "checksum", "version_id"):
        if key in normalized:
            normalized[key] = _normalize_etag(normalized[key])
    for key in ("key", "object_key", "name", "path"):
        if key in normalized:
            normalized[key] = _normalize_storage_key(normalized[key])
    return normalized


def normalize_object_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    for key in ("created_at", "updated_at", "last_modified", "expires_at"):
        if key in normalized:
            normalized[key] = _normalize_datetime(normalized[key])
    if "metadata" in normalized and isinstance(normalized["metadata"], Mapping):
        normalized["metadata"] = normalize_object_metadata(normalized["metadata"])
    return normalized


def build_object_url(bucket: str, key: str, *, endpoint: Optional[str] = None, scheme: str = "https") -> str:
    safe_key = "/".join(quote(part, safe="") for part in _normalize_storage_key(key).split("/"))
    if endpoint:
        parsed = urlparse(endpoint)
        if parsed.scheme and parsed.netloc:
            base = endpoint.rstrip("/")
            return f"{base}/{quote(bucket, safe='')}/{safe_key}"
        return f"{scheme}://{endpoint.strip('/').rstrip('/')}/{quote(bucket, safe='')}/{safe_key}"
    return f"{scheme}://storage.example.com/{quote(bucket, safe='')}/{safe_key}"


@dataclass(slots=True)
class StorageObjectRequest:
    bucket: str
    key: str
    version_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        if self.version_id is not None:
            self.version_id = _normalize_etag(self.version_id)


@dataclass(slots=True)
class StorageObjectResponse:
    bucket: str
    key: str
    etag: str | None = None
    size: int | None = None
    last_modified: datetime | None = None
    content_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        self.etag = _normalize_etag(self.etag)
        self.last_modified = _normalize_datetime(self.last_modified)
        self.metadata = normalize_object_metadata(self.metadata)


@dataclass(slots=True)
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    continuation_token: str | None = None
    max_results: int | None = None

    def __post_init__(self) -> None:
        self.prefix = _normalize_storage_key(self.prefix)


@dataclass(slots=True)
class PresignedUrlResponse:
    bucket: str
    key: str
    url: str
    expires_at: datetime | None = None
    method: str = "GET"

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        self.expires_at = _normalize_datetime(self.expires_at)


@dataclass(slots=True)
class ObjectListItem:
    bucket: str
    key: str
    size: int | None = None
    last_modified: datetime | None = None
    etag: str | None = None

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        self.last_modified = _normalize_datetime(self.last_modified)
        self.etag = _normalize_etag(self.etag)


@dataclass(slots=True)
class ObjectListResponse:
    bucket: str
    prefix: str = ""
    items: list[ObjectListItem] = field(default_factory=list)
    next_continuation_token: str | None = None
    is_truncated: bool = False

    def __post_init__(self) -> None:
        self.prefix = _normalize_storage_key(self.prefix)
        self.items = [item if isinstance(item, ObjectListItem) else ObjectListItem(**item) for item in self.items]


@dataclass(slots=True)
class ObjectMetadataResponse:
    bucket: str
    key: str
    exists: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        self.metadata = normalize_object_metadata(self.metadata)


@dataclass(slots=True)
class UploadResult:
    bucket: str
    key: str
    etag: str | None = None
    version_id: str | None = None
    url: str | None = None

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        self.etag = _normalize_etag(self.etag)
        self.version_id = _normalize_etag(self.version_id)


@dataclass(slots=True)
class StoredAssetSummary:
    bucket: str
    key: str
    title: str | None = None
    summary: str | None = None
    extracted_text: str | None = None
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.key = _normalize_storage_key(self.key)
        self.metadata = normalize_object_metadata(self.metadata)
