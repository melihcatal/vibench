from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


def _to_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _normalize_datetime(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        try:
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return text
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_metadata(metadata: Any) -> dict:
    if metadata is None:
        return {}
    if isinstance(metadata, Mapping):
        return {str(key): _to_str(value) for key, value in metadata.items() if _to_str(value) is not None}
    return {}


@dataclass(frozen=True)
class StorageObjectRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    cache_control: Optional[str] = None
    content_disposition: Optional[str] = None
    storage_class: Optional[str] = None

    def to_dict(self) -> dict:
        payload = {
            "bucket": self.bucket,
            "key": self.key,
            "content_type": self.content_type,
            "metadata": self.metadata or {},
            "cache_control": self.cache_control,
            "content_disposition": self.content_disposition,
            "storage_class": self.storage_class,
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(frozen=True)
class StorageObjectResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    version_id: Optional[str] = None

    def to_dict(self) -> dict:
        payload = {
            "bucket": self.bucket,
            "key": self.key,
            "etag": self.etag,
            "content_length": self.content_length,
            "content_type": self.content_type,
            "last_modified": self.last_modified,
            "storage_class": self.storage_class,
            "metadata": self.metadata or {},
            "version_id": self.version_id,
        }
        return {k: v for k, v in payload.items() if v is not None}


def normalize_object_response(bucket: str, key: str, response: Mapping[str, Any]) -> StorageObjectResponse:
    return StorageObjectResponse(
        bucket=bucket,
        key=key,
        etag=_to_str(response.get("ETag") or response.get("etag")),
        content_length=_to_int(response.get("ContentLength") or response.get("content_length")),
        content_type=_to_str(response.get("ContentType") or response.get("content_type")),
        last_modified=_normalize_datetime(response.get("LastModified") or response.get("last_modified")),
        storage_class=_to_str(response.get("StorageClass") or response.get("storage_class")),
        metadata=normalize_metadata(response.get("Metadata") or response.get("metadata")),
        version_id=_to_str(response.get("VersionId") or response.get("version_id")),
    )


def build_object_upload_request(
    bucket: str,
    key: str,
    content_type: Optional[str] = None,
    metadata: Optional[Mapping[str, Any]] = None,
    cache_control: Optional[str] = None,
    content_disposition: Optional[str] = None,
    storage_class: Optional[str] = None,
) -> StorageObjectRequest:
    return StorageObjectRequest(
        bucket=bucket,
        key=key,
        content_type=_to_str(content_type),
        metadata=normalize_metadata(metadata),
        cache_control=_to_str(cache_control),
        content_disposition=_to_str(content_disposition),
        storage_class=_to_str(storage_class),
    )
