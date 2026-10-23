from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


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
    checksum_sha256: Optional[str] = None


@dataclass(slots=True)
class ObjectMetadataResult:
    bucket: str
    key: str
    size: Optional[int]
    etag: Optional[str]
    content_type: Optional[str]
    last_modified: Optional[datetime]
    metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int
    etag: Optional[str]
    last_modified: Optional[datetime]
    storage_class: Optional[str] = None


@dataclass(slots=True)
class OCRResult:
    object_ref: StorageObjectRef
    text: str
    page_count: int
    provider_job_id: Optional[str] = None
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider_request_id: Optional[str] = None


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider_response_id: Optional[str] = None


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    model: str
    dimensions: int



def normalize_s3_metadata(response: Dict[str, Any]) -> ObjectMetadataResult:
    return ObjectMetadataResult(
        bucket=response.get("Bucket", ""),
        key=response.get("Key", ""),
        size=response.get("ContentLength"),
        etag=(response.get("ETag") or "").strip('"') or None,
        content_type=response.get("ContentType"),
        last_modified=response.get("LastModified"),
        metadata=response.get("Metadata") or {},
        version_id=response.get("VersionId"),
        storage_class=response.get("StorageClass"),
    )



def normalize_s3_list(contents: Iterable[Dict[str, Any]]) -> List[ListedObject]:
    items: List[ListedObject] = []
    for item in contents:
        items.append(
            ListedObject(
                key=item["Key"],
                size=item.get("Size", 0),
                etag=(item.get("ETag") or "").strip('"') or None,
                last_modified=item.get("LastModified"),
                storage_class=item.get("StorageClass"),
            )
        )
    return items
