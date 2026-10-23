from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class StorageObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class UploadObjectRequest:
    bucket: str
    key: str
    body: bytes | str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadObjectResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    checksum: Optional[str]
    url: str


@dataclass
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    response_content_type: Optional[str] = None


@dataclass
class ObjectMetadataResult:
    bucket: str
    key: str
    size: Optional[int]
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str]
    version_id: Optional[str]


@dataclass
class ListedObject:
    key: str
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str]


@dataclass
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    next_token: Optional[str]


@dataclass
class OCRResult:
    source_bucket: str
    source_key: str
    job_status: str
    text: str
    page_count: int
    provider_job_id: str


@dataclass
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str
    provider: str


@dataclass
class SummaryResult:
    summary: str
    model: str
    provider: str


@dataclass
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    model: str
    provider: str


def normalize_datetime(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def normalize_s3_head(
    bucket: str, key: str, response: Dict[str, Any]
) -> ObjectMetadataResult:
    return ObjectMetadataResult(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=normalize_datetime(response.get("LastModified")),
        metadata=response.get("Metadata", {}) or {},
        version_id=response.get("VersionId"),
    )


def normalize_s3_list(
    bucket: str, prefix: str, response: Dict[str, Any]
) -> ListPrefixResult:
    contents = response.get("Contents", []) or []
    objects = [
        ListedObject(
            key=item["Key"],
            size=item.get("Size"),
            etag=item.get("ETag"),
            last_modified=normalize_datetime(item.get("LastModified")),
            storage_class=item.get("StorageClass"),
        )
        for item in contents
    ]
    return ListPrefixResult(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        next_token=response.get("NextContinuationToken"),
    )
