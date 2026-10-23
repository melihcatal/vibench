from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


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
    metadata: Optional[Dict[str, str]] = None


@dataclass(slots=True)
class UploadObjectResult:
    bucket: str
    key: str
    etag: Optional[str]
    version_id: Optional[str]
    checksum_sha256: Optional[str]


@dataclass(slots=True)
class PresignedDownloadRequest:
    bucket: str
    key: str
    expires_in: int = 3600
    response_content_type: Optional[str] = None


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
    metadata: Dict[str, str]
    version_id: Optional[str]


@dataclass(slots=True)
class ListedObject:
    key: str
    size: Optional[int]
    etag: Optional[str]
    last_modified: Optional[str]
    storage_class: Optional[str]


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject]
    next_continuation_token: Optional[str]


@dataclass(slots=True)
class OCRResult:
    bucket: str
    key: str
    text: str
    page_count: int
    raw_blocks: List[Dict[str, Any]]


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str]
    target_language: str


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str
    provider: str


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    model: str
    provider: str


def normalize_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = (
            value.astimezone(timezone.utc)
            if value.tzinfo
            else value.replace(tzinfo=timezone.utc)
        )
        return dt.isoformat()
    return str(value)


def coerce_metadata(value: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(k): str(v) for k, v in value.items()}


def build_embedding_input(metadata: ObjectMetadataResult, extracted_text: str) -> str:
    metadata_lines = [
        f"bucket={metadata.bucket}",
        f"key={metadata.key}",
        f"size={metadata.size}",
        f"etag={metadata.etag}",
        f"content_type={metadata.content_type}",
        f"last_modified={metadata.last_modified}",
    ]
    for key, value in sorted(metadata.metadata.items()):
        metadata_lines.append(f"meta.{key}={value}")
    return "\n".join(metadata_lines + ["", extracted_text.strip()])
