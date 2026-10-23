from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union


JsonDict = Dict[str, Any]


def _to_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        normalized[str(key)] = _to_str(value) or ""
    return normalized


def normalize_object_key(key: Any) -> str:
    value = _to_str(key)
    if value is None or value == "":
        raise ValueError("object key is required")
    return value.lstrip("/")


def normalize_container_name(name: Any) -> str:
    value = _to_str(name)
    if value is None or value == "":
        raise ValueError("container name is required")
    return value.strip()


@dataclass(frozen=True)
class StorageObjectRef:
    container: str
    key: str

    @classmethod
    def from_values(cls, container: Any, key: Any) -> "StorageObjectRef":
        return cls(container=normalize_container_name(container), key=normalize_object_key(key))


@dataclass(frozen=True)
class UploadObjectRequest:
    container: str
    key: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    cache_control: Optional[str] = None
    content_disposition: Optional[str] = None
    content_encoding: Optional[str] = None
    content_language: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "UploadObjectRequest":
        return cls(
            container=normalize_container_name(data.get("container")),
            key=normalize_object_key(data.get("key")),
            content_type=_to_str(data.get("content_type")),
            metadata=normalize_metadata(data.get("metadata")),
            cache_control=_to_str(data.get("cache_control")),
            content_disposition=_to_str(data.get("content_disposition")),
            content_encoding=_to_str(data.get("content_encoding")),
            content_language=_to_str(data.get("content_language")),
        )


@dataclass(frozen=True)
class ObjectHeadResponse:
    container: str
    key: str
    etag: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    metadata: Dict[str, str] = None  # type: ignore[assignment]
    version_id: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "ObjectHeadResponse":
        container = normalize_container_name(data.get("container") or data.get("bucket"))
        key = normalize_object_key(data.get("key") or data.get("name") or data.get("object_key"))
        size_value = data.get("size") or data.get("content_length")
        try:
            size = int(size_value) if size_value is not None else None
        except (TypeError, ValueError):
            size = None
        return cls(
            container=container,
            key=key,
            etag=_to_str(data.get("etag") or data.get("ETag")),
            size=size,
            content_type=_to_str(data.get("content_type") or data.get("Content-Type")),
            last_modified=_coerce_datetime(data.get("last_modified") or data.get("Last-Modified") or data.get("updated_at")),
            metadata=normalize_metadata(data.get("metadata")),
            version_id=_to_str(data.get("version_id") or data.get("versionId")),
        )


@dataclass(frozen=True)
class ListPrefixRequest:
    container: str
    prefix: str = ""
    delimiter: Optional[str] = None
    max_keys: Optional[int] = None
    continuation_token: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ListPrefixRequest":
        return cls(
            container=normalize_container_name(data.get("container")),
            prefix=_to_str(data.get("prefix")) or "",
            delimiter=_to_str(data.get("delimiter")),
            max_keys=int(data["max_keys"]) if data.get("max_keys") is not None else None,
            continuation_token=_to_str(data.get("continuation_token")),
        )


@dataclass(frozen=True)
class ListedObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "ListedObject":
        size_value = data.get("size") or data.get("content_length")
        try:
            size = int(size_value) if size_value is not None else None
        except (TypeError, ValueError):
            size = None
        return cls(
            key=normalize_object_key(data.get("key") or data.get("name") or data.get("object_key")),
            size=size,
            last_modified=_coerce_datetime(data.get("last_modified") or data.get("updated_at")),
            etag=_to_str(data.get("etag") or data.get("ETag")),
            storage_class=_to_str(data.get("storage_class") or data.get("class")),
        )


@dataclass(frozen=True)
class ListPrefixResponse:
    container: str
    prefix: str
    objects: List[ListedObject]
    common_prefixes: List[str]
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "ListPrefixResponse":
        objects_data = data.get("objects") or data.get("contents") or []
        common_prefixes = data.get("common_prefixes") or data.get("prefixes") or []
        return cls(
            container=normalize_container_name(data.get("container") or data.get("bucket")),
            prefix=_to_str(data.get("prefix")) or "",
            objects=[ListedObject.from_provider(item) for item in objects_data],
            common_prefixes=[_to_str(item) or "" for item in common_prefixes if _to_str(item)],
            is_truncated=bool(data.get("is_truncated") or data.get("truncated")),
            next_continuation_token=_to_str(data.get("next_continuation_token") or data.get("next_token")),
        )


@dataclass(frozen=True)
class PresignedUrlResponse:
    url: str
    expires_at: Optional[datetime] = None
    method: str = "GET"

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "PresignedUrlResponse":
        return cls(
            url=_to_str(data.get("url") or data.get("signed_url") or data.get("presigned_url")) or "",
            expires_at=_coerce_datetime(data.get("expires_at") or data.get("expiration")),
            method=(_to_str(data.get("method")) or "GET").upper(),
        )


@dataclass(frozen=True)
class ObjectMetadataResponse:
    container: str
    key: str
    metadata: Dict[str, str]
    content_type: Optional[str] = None
    size: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "ObjectMetadataResponse":
        size_value = data.get("size") or data.get("content_length")
        try:
            size = int(size_value) if size_value is not None else None
        except (TypeError, ValueError):
            size = None
        return cls(
            container=normalize_container_name(data.get("container") or data.get("bucket")),
            key=normalize_object_key(data.get("key") or data.get("name") or data.get("object_key")),
            metadata=normalize_metadata(data.get("metadata")),
            content_type=_to_str(data.get("content_type") or data.get("Content-Type")),
            size=size,
            etag=_to_str(data.get("etag") or data.get("ETag")),
            last_modified=_coerce_datetime(data.get("last_modified") or data.get("updated_at")),
        )


@dataclass(frozen=True)
class UploadObjectResponse:
    container: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "UploadObjectResponse":
        size_value = data.get("size") or data.get("content_length")
        try:
            size = int(size_value) if size_value is not None else None
        except (TypeError, ValueError):
            size = None
        return cls(
            container=normalize_container_name(data.get("container") or data.get("bucket")),
            key=normalize_object_key(data.get("key") or data.get("name") or data.get("object_key")),
            etag=_to_str(data.get("etag") or data.get("ETag")),
            version_id=_to_str(data.get("version_id") or data.get("versionId")),
            size=size,
            content_type=_to_str(data.get("content_type") or data.get("Content-Type")),
        )


@dataclass(frozen=True)
class AssetSummary:
    container: str
    key: str
    summary: str
    confidence: Optional[float] = None
    language: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "AssetSummary":
        confidence = data.get("confidence")
        try:
            confidence_value = float(confidence) if confidence is not None else None
        except (TypeError, ValueError):
            confidence_value = None
        return cls(
            container=normalize_container_name(data.get("container") or data.get("bucket")),
            key=normalize_object_key(data.get("key") or data.get("name") or data.get("object_key")),
            summary=_to_str(data.get("summary") or data.get("text") or "") or "",
            confidence=confidence_value,
            language=_to_str(data.get("language") or data.get("lang")),
        )


@dataclass(frozen=True)
class OcrResult:
    container: str
    key: str
    text: str
    pages: Optional[int] = None
    language: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "OcrResult":
        pages_value = data.get("pages")
        try:
            pages = int(pages_value) if pages_value is not None else None
        except (TypeError, ValueError):
            pages = None
        return cls(
            container=normalize_container_name(data.get("container") or data.get("bucket")),
            key=normalize_object_key(data.get("key") or data.get("name") or data.get("object_key")),
            text=_to_str(data.get("text") or data.get("ocr_text") or "") or "",
            pages=pages,
            language=_to_str(data.get("language") or data.get("lang")),
        )


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None

    @classmethod
    def from_provider(cls, data: Mapping[str, Any]) -> "TranslationResult":
        return cls(
            source_text=_to_str(data.get("source_text") or data.get("text") or "") or "",
            translated_text=_to_str(data.get("translated_text") or data.get("translation") or "") or "",
            source_language=_to_str(data.get("source_language") or data.get("from_language")),
            target_language=_to_str(data.get("target_language") or data.get("to_language")),
        )


def normalize_sequence_of_strings(values: Optional[Sequence[Any]]) -> List[str]:
    if not values:
        return []
    out: List[str] = []
    for value in values:
        text = _to_str(value)
        if text:
            out.append(text)
    return out


def normalize_mapping_of_strings(values: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    return normalize_metadata(values)
