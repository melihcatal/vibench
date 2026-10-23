from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union
import base64
import hashlib
import json


def _to_utc_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            return None
    else:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _stringify(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, datetime):
        return _to_utc_datetime(value).isoformat().replace("+00:00", "Z") if _to_utc_datetime(value) else None
    if isinstance(value, Mapping):
        return {str(k): _stringify(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_stringify(v) for v in value]
    return str(value)


def normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    normalized: Dict[str, str] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        normalized[str(key).lower()] = str(_stringify(value))
    return normalized


def normalize_tags(tags: Optional[Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]]) -> Dict[str, str]:
    if not tags:
        return {}
    if isinstance(tags, Mapping):
        return {str(k): str(_stringify(v)) for k, v in tags.items() if v is not None}
    normalized: Dict[str, str] = {}
    for item in tags:
        if not isinstance(item, Mapping):
            continue
        key = item.get("key") or item.get("name")
        value = item.get("value")
        if key is None or value is None:
            continue
        normalized[str(key)] = str(_stringify(value))
    return normalized


def normalize_etag(etag: Optional[str]) -> Optional[str]:
    if etag is None:
        return None
    text = str(etag).strip()
    if not text:
        return None
    if text.startswith('"') and text.endswith('"') and len(text) >= 2:
        return text[1:-1]
    return text


def normalize_content_type(content_type: Optional[str]) -> Optional[str]:
    if content_type is None:
        return None
    text = str(content_type).strip()
    return text or None


def normalize_object_key(bucket: Optional[str], key: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    bucket_text = str(bucket).strip() if bucket is not None else None
    key_text = str(key).strip() if key is not None else None
    return (bucket_text or None, key_text or None)


def normalize_response_payload(payload: Any) -> Any:
    if payload is None:
        return None
    if isinstance(payload, bytes):
        try:
            return json.loads(payload.decode("utf-8"))
        except Exception:
            return payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        text = payload.strip()
        if not text:
            return payload
        try:
            return json.loads(text)
        except Exception:
            return payload
    if isinstance(payload, Mapping):
        return {str(k): normalize_response_payload(v) for k, v in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [normalize_response_payload(v) for v in payload]
    if isinstance(payload, datetime):
        dt = _to_utc_datetime(payload)
        return dt.isoformat().replace("+00:00", "Z") if dt else None
    return payload


def ensure_bytes(data: Union[str, bytes, bytearray, memoryview]) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    if isinstance(data, str):
        return data.encode("utf-8")
    raise TypeError("data must be str or bytes-like")


def content_md5(data: Union[str, bytes, bytearray, memoryview]) -> str:
    blob = ensure_bytes(data)
    return base64.b64encode(hashlib.md5(blob).digest()).decode("ascii")


@dataclass(frozen=True)
class ObjectReference:
    bucket: str
    key: str

    def normalized(self) -> "ObjectReference":
        bucket, key = normalize_object_key(self.bucket, self.key)
        return ObjectReference(bucket=bucket or "", key=key or "")


@dataclass(frozen=True)
class StoredObjectInfo:
    bucket: str
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "StoredObjectInfo":
        return cls(
            bucket=str(data.get("bucket") or data.get("container") or ""),
            key=str(data.get("key") or data.get("name") or ""),
            size=int(data["size"]) if data.get("size") is not None else None,
            etag=normalize_etag(data.get("etag")),
            content_type=normalize_content_type(data.get("content_type") or data.get("contentType")),
            last_modified=_to_utc_datetime(data.get("last_modified") or data.get("lastModified") or data.get("updated_at")),
            metadata=normalize_metadata(data.get("metadata")),
            tags=normalize_tags(data.get("tags")),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "bucket": self.bucket,
            "key": self.key,
            "metadata": dict(self.metadata),
            "tags": dict(self.tags),
        }
        if self.size is not None:
            result["size"] = self.size
        if self.etag is not None:
            result["etag"] = self.etag
        if self.content_type is not None:
            result["content_type"] = self.content_type
        if self.last_modified is not None:
            result["last_modified"] = self.last_modified.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return result


@dataclass(frozen=True)
class UploadObjectRequest:
    bucket: str
    key: str
    body: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "UploadObjectRequest":
        body = payload.get("body")
        return cls(
            bucket=str(payload.get("bucket") or ""),
            key=str(payload.get("key") or ""),
            body=ensure_bytes(body) if body is not None and not isinstance(body, bytes) else body,
            content_type=normalize_content_type(payload.get("content_type") or payload.get("contentType")),
            metadata=normalize_metadata(payload.get("metadata")),
            tags=normalize_tags(payload.get("tags")),
        )


@dataclass(frozen=True)
class UploadObjectResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    checksum_md5: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UploadObjectResponse":
        return cls(
            bucket=str(data.get("bucket") or ""),
            key=str(data.get("key") or ""),
            etag=normalize_etag(data.get("etag")),
            version_id=str(data.get("version_id") or data.get("versionId") or "") or None,
            checksum_md5=str(data.get("checksum_md5") or data.get("content_md5") or "") or None,
        )


@dataclass(frozen=True)
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: Optional[str] = None
    max_items: Optional[int] = None
    continuation_token: Optional[str] = None

    def to_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"bucket": self.bucket, "prefix": self.prefix}
        if self.delimiter is not None:
            params["delimiter"] = self.delimiter
        if self.max_items is not None:
            params["max_items"] = self.max_items
        if self.continuation_token is not None:
            params["continuation_token"] = self.continuation_token
        return params


@dataclass(frozen=True)
class ListPrefixResponse:
    items: List[StoredObjectInfo] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    next_continuation_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ListPrefixResponse":
        items_data = data.get("items") or data.get("objects") or []
        items = [StoredObjectInfo.from_dict(item) for item in items_data if isinstance(item, Mapping)]
        prefixes = data.get("common_prefixes") or data.get("prefixes") or []
        return cls(
            items=items,
            common_prefixes=[str(p) for p in prefixes],
            next_continuation_token=str(data.get("next_continuation_token") or data.get("nextToken") or "") or None,
        )


@dataclass(frozen=True)
class ObjectMetadataRequest:
    bucket: str
    key: str


@dataclass(frozen=True)
class ObjectMetadataResponse:
    object_info: StoredObjectInfo
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ObjectMetadataResponse":
        info = StoredObjectInfo.from_dict(data)
        return cls(object_info=info, raw=dict(data))


@dataclass(frozen=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    response_content_type: Optional[str] = None
    response_content_disposition: Optional[str] = None


@dataclass(frozen=True)
class PresignedDownloadResponse:
    url: str
    expires_at: Optional[datetime] = None


@dataclass(frozen=True)
class AssetSummaryRequest:
    bucket: str
    key: str
    language: Optional[str] = None
    max_sentences: Optional[int] = None


@dataclass(frozen=True)
class AssetSummaryResponse:
    summary: str
    language: Optional[str] = None
    source: Optional[str] = None


@dataclass(frozen=True)
class OCRRequest:
    bucket: str
    key: str
    language: Optional[str] = None
    page_numbers: Optional[List[int]] = None


@dataclass(frozen=True)
class OCRResponse:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class TranslateTextRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass(frozen=True)
class TranslateTextResponse:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass(frozen=True)
class MetadataEmbeddingRequest:
    bucket: str
    key: str
    extracted_text: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    embedding_model: Optional[str] = None


@dataclass(frozen=True)
class MetadataEmbeddingResponse:
    vector: List[float]
    dimensions: Optional[int] = None
    model: Optional[str] = None


def normalize_list_response_items(items: Iterable[Mapping[str, Any]]) -> List[StoredObjectInfo]:
    return [StoredObjectInfo.from_dict(item) for item in items if isinstance(item, Mapping)]
