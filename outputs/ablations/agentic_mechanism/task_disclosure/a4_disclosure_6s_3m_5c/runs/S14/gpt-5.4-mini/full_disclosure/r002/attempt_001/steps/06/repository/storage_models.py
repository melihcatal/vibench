from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional


def _normalize_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    text = str(value).strip()
    return text or None


def _normalize_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = _normalize_string(value)
    if text is None:
        return None
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def _normalize_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    text = _normalize_string(value)
    if text is None:
        return None
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _normalize_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = _normalize_string(value)
    if text is None:
        return None
    lowered = text.lower()
    if lowered in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "f", "no", "n", "off"}:
        return False
    return None


def _normalize_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    text = _normalize_string(value)
    if text is None:
        return None
    try:
        normalized = text.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _normalize_mapping(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {str(k): v for k, v in value.items() if v is not None}
    return {}


def normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in metadata.items():
        k = _normalize_string(key)
        v = _normalize_string(value)
        if k is not None and v is not None:
            normalized[k] = v
    return normalized


def normalize_object_reference(value: Any) -> Dict[str, Any]:
    if isinstance(value, ObjectReference):
        return value.to_dict()
    if isinstance(value, Mapping):
        return {
            "bucket": _normalize_string(value.get("bucket")),
            "key": _normalize_string(value.get("key")),
            "version_id": _normalize_string(value.get("version_id") or value.get("versionId")),
        }
    return {"bucket": None, "key": None, "version_id": None}


@dataclass(frozen=True)
class ObjectReference:
    bucket: Optional[str]
    key: Optional[str]
    version_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ObjectReference":
        normalized = normalize_object_reference(data)
        return cls(
            bucket=normalized.get("bucket"),
            key=normalized.get("key"),
            version_id=normalized.get("version_id"),
        )

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {"bucket": self.bucket, "key": self.key, "version_id": self.version_id}


@dataclass(frozen=True)
class StoredObjectMetadata:
    bucket: Optional[str] = None
    key: Optional[str] = None
    etag: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    content_encoding: Optional[str] = None
    content_language: Optional[str] = None
    cache_control: Optional[str] = None
    content_disposition: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    checksum: Optional[str] = None
    custom_metadata: Dict[str, str] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "StoredObjectMetadata":
        mapping = dict(data or {})
        return cls(
            bucket=_normalize_string(mapping.get("bucket") or mapping.get("Bucket")),
            key=_normalize_string(mapping.get("key") or mapping.get("Key")),
            etag=_normalize_string(mapping.get("etag") or mapping.get("ETag")),
            size=_normalize_int(mapping.get("size") or mapping.get("ContentLength") or mapping.get("content_length")),
            content_type=_normalize_string(mapping.get("content_type") or mapping.get("ContentType")),
            content_encoding=_normalize_string(mapping.get("content_encoding") or mapping.get("ContentEncoding")),
            content_language=_normalize_string(mapping.get("content_language") or mapping.get("ContentLanguage")),
            cache_control=_normalize_string(mapping.get("cache_control") or mapping.get("CacheControl")),
            content_disposition=_normalize_string(mapping.get("content_disposition") or mapping.get("ContentDisposition")),
            last_modified=_normalize_datetime(mapping.get("last_modified") or mapping.get("LastModified")),
            storage_class=_normalize_string(mapping.get("storage_class") or mapping.get("StorageClass")),
            version_id=_normalize_string(mapping.get("version_id") or mapping.get("VersionId")),
            checksum=_normalize_string(
                mapping.get("checksum")
                or mapping.get("Checksum")
                or mapping.get("sha256")
                or mapping.get("md5")
            ),
            custom_metadata=normalize_metadata(
                mapping.get("custom_metadata") or mapping.get("Metadata") or mapping.get("metadata")
            ),
            raw=mapping,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "key": self.key,
            "etag": self.etag,
            "size": self.size,
            "content_type": self.content_type,
            "content_encoding": self.content_encoding,
            "content_language": self.content_language,
            "cache_control": self.cache_control,
            "content_disposition": self.content_disposition,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "storage_class": self.storage_class,
            "version_id": self.version_id,
            "checksum": self.checksum,
            "custom_metadata": dict(self.custom_metadata),
        }


@dataclass(frozen=True)
class ManagedObjectListResult:
    items: tuple[StoredObjectMetadata, ...] = ()
    prefix: Optional[str] = None
    next_token: Optional[str] = None
    truncated: Optional[bool] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ManagedObjectListResult":
        mapping = dict(data or {})
        items_value = mapping.get("items") or mapping.get("Contents") or mapping.get("objects") or []
        items = tuple(
            item if isinstance(item, StoredObjectMetadata) else StoredObjectMetadata.from_dict(item)
            for item in items_value
            if item is not None
        )
        return cls(
            items=items,
            prefix=_normalize_string(mapping.get("prefix") or mapping.get("Prefix")),
            next_token=_normalize_string(
                mapping.get("next_token") or mapping.get("NextToken") or mapping.get("continuation_token")
            ),
            truncated=_normalize_bool(mapping.get("truncated") or mapping.get("IsTruncated")),
            raw=mapping,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "items": [item.to_dict() for item in self.items],
            "prefix": self.prefix,
            "next_token": self.next_token,
            "truncated": self.truncated,
        }


@dataclass(frozen=True)
class UploadObjectRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    storage_class: Optional[str] = None
    checksum: Optional[str] = None
    server_side_encryption: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UploadObjectRequest":
        mapping = dict(data or {})
        return cls(
            bucket=_normalize_string(mapping.get("bucket")) or "",
            key=_normalize_string(mapping.get("key")) or "",
            content_type=_normalize_string(mapping.get("content_type") or mapping.get("ContentType")),
            metadata=normalize_metadata(mapping.get("metadata") or mapping.get("Metadata")),
            tags=normalize_metadata(mapping.get("tags") or mapping.get("Tags")),
            storage_class=_normalize_string(mapping.get("storage_class") or mapping.get("StorageClass")),
            checksum=_normalize_string(mapping.get("checksum") or mapping.get("Checksum")),
            server_side_encryption=_normalize_string(
                mapping.get("server_side_encryption") or mapping.get("ServerSideEncryption")
            ),
        )


@dataclass(frozen=True)
class UploadObjectResult:
    bucket: Optional[str] = None
    key: Optional[str] = None
    etag: Optional[str] = None
    version_id: Optional[str] = None
    checksum: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UploadObjectResult":
        mapping = dict(data or {})
        return cls(
            bucket=_normalize_string(mapping.get("bucket") or mapping.get("Bucket")),
            key=_normalize_string(mapping.get("key") or mapping.get("Key")),
            etag=_normalize_string(mapping.get("etag") or mapping.get("ETag")),
            version_id=_normalize_string(mapping.get("version_id") or mapping.get("VersionId")),
            checksum=_normalize_string(mapping.get("checksum") or mapping.get("Checksum")),
            raw=mapping,
        )


@dataclass(frozen=True)
class PresignedUrlResult:
    url: str
    expires_in: Optional[int] = None
    method: Optional[str] = None
    bucket: Optional[str] = None
    key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PresignedUrlResult":
        mapping = dict(data or {})
        return cls(
            url=_normalize_string(mapping.get("url") or mapping.get("Url") or "") or "",
            expires_in=_normalize_int(mapping.get("expires_in") or mapping.get("ExpiresIn")),
            method=_normalize_string(mapping.get("method") or mapping.get("Method")),
            bucket=_normalize_string(mapping.get("bucket") or mapping.get("Bucket")),
            key=_normalize_string(mapping.get("key") or mapping.get("Key")),
        )


@dataclass(frozen=True)
class ObjectHeadResult:
    metadata: StoredObjectMetadata
    exists: bool = True

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ObjectHeadResult":
        mapping = dict(data or {})
        exists = _normalize_bool(mapping.get("exists") or mapping.get("Exists"))
        if exists is None:
            exists = True
        return cls(metadata=StoredObjectMetadata.from_dict(mapping), exists=exists)


@dataclass(frozen=True)
class DocumentTextResult:
    text: str = ""
    language: Optional[str] = None
    page_count: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "DocumentTextResult":
        mapping = dict(data or {})
        return cls(
            text=_normalize_string(mapping.get("text") or mapping.get("Text") or "") or "",
            language=_normalize_string(mapping.get("language") or mapping.get("Language")),
            page_count=_normalize_int(mapping.get("page_count") or mapping.get("PageCount")),
            raw=mapping,
        )


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str = ""
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranslationResult":
        mapping = dict(data or {})
        return cls(
            translated_text=_normalize_string(mapping.get("translated_text") or mapping.get("TranslatedText") or "")
            or "",
            source_language=_normalize_string(mapping.get("source_language") or mapping.get("SourceLanguage")),
            target_language=_normalize_string(mapping.get("target_language") or mapping.get("TargetLanguage")),
            raw=mapping,
        )


@dataclass(frozen=True)
class SummaryResult:
    summary: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SummaryResult":
        mapping = dict(data or {})
        return cls(summary=_normalize_string(mapping.get("summary") or mapping.get("Summary") or "") or "", raw=mapping)


@dataclass(frozen=True)
class EmbeddingResult:
    vector: tuple[float, ...] = ()
    dimensions: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EmbeddingResult":
        mapping = dict(data or {})
        vector_value = mapping.get("vector") or mapping.get("embedding") or mapping.get("Embedding") or []
        vector = tuple(float(v) for v in vector_value if v is not None)
        return cls(vector=vector, dimensions=len(vector) if vector else None, raw=mapping)
