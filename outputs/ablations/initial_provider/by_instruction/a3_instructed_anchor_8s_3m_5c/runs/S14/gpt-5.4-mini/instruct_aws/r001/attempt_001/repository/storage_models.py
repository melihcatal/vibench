from dataclasses import dataclass
from typing import Any, Mapping, Optional


def _text(value: Any) -> str:
    return "" if value is None else str(value)


def _int(value: Any) -> Optional[int]:
    if value is None:
        return None
    return int(value)


@dataclass
class StorageObjectRef:
    bucket: str
    key: str


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: Any
    content_type: Optional[str] = None
    metadata: Optional[Mapping[str, str]] = None


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class MetadataResponse:
    bucket: str
    key: str
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[Any] = None
    metadata: Optional[Mapping[str, str]] = None


@dataclass
class ListResponse:
    bucket: str
    prefix: str
    keys: list[str]


@dataclass
class PresignedUrlResponse:
    bucket: str
    key: str
    url: str
    expires_in: int


@dataclass
class OCRResponse:
    bucket: str
    key: str
    text: str


@dataclass
class TranslationResponse:
    source_language: str
    target_language: str
    text: str


@dataclass
class SummaryResponse:
    text: str
    summary: str


@dataclass
class EmbeddingResponse:
    bucket: str
    key: str
    vector: list[float]


def normalize_head_response(bucket: str, key: str, head: Mapping[str, Any]) -> MetadataResponse:
    return MetadataResponse(
        bucket=bucket,
        key=key,
        content_length=_int(head.get("ContentLength")),
        content_type=_text(head.get("ContentType")) or None,
        etag=_text(head.get("ETag")) or None,
        last_modified=head.get("LastModified"),
        metadata=head.get("Metadata") or None,
    )


def normalize_list_keys(bucket: str, prefix: str, items: list[Mapping[str, Any]]) -> ListResponse:
    return ListResponse(bucket=bucket, prefix=prefix, keys=[_text(item.get("Key")) for item in items if item.get("Key")])
