from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str


@dataclass(slots=True)
class UploadObjectRequest:
    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UploadObjectResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    response_content_type: Optional[str] = None
    response_content_disposition: Optional[str] = None


@dataclass(slots=True)
class PresignedDownloadResult:
    bucket: str
    key: str
    url: str
    expires_in: int


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket: str
    key: str
    size: Optional[int]
    etag: Optional[str]
    content_type: Optional[str]
    last_modified: Optional[str]
    version_id: Optional[str]
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    max_keys: int = 1000
    continuation_token: Optional[str] = None


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int
    etag: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str]


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    is_truncated: bool
    next_continuation_token: Optional[str]


@dataclass(slots=True)
class StoredDocumentOcrResult:
    bucket: str
    key: str
    text: str
    page_count: int
    provider: str
    model: str


@dataclass(slots=True)
class StoredTextTranslateResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str
    provider: str


@dataclass(slots=True)
class StoredAssetSummaryResult:
    summary: str
    provider: str
    model: str


@dataclass(slots=True)
class AssetMetadataEmbeddingResult:
    vector: List[float]
    dimensions: int
    provider: str
    model: str


def isoformat_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    return str(value)


def normalize_s3_head(
    bucket: str, key: str, response: Mapping[str, Any]
) -> ObjectMetadataResult:
    return ObjectMetadataResult(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        etag=_strip_quotes(response.get("ETag")),
        content_type=response.get("ContentType"),
        last_modified=isoformat_or_none(response.get("LastModified")),
        version_id=response.get("VersionId"),
        metadata=dict(response.get("Metadata") or {}),
    )


def normalize_s3_list(
    bucket: str, prefix: str, response: Mapping[str, Any]
) -> ListPrefixResult:
    objects = [
        ListedObject(
            key=item["Key"],
            size=int(item.get("Size", 0)),
            etag=_strip_quotes(item.get("ETag")),
            last_modified=isoformat_or_none(item.get("LastModified")),
            storage_class=item.get("StorageClass"),
        )
        for item in response.get("Contents", [])
    ]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        is_truncated=bool(response.get("IsTruncated")),
        next_continuation_token=response.get("NextContinuationToken"),
    )


def _strip_quotes(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return value.strip('"')
