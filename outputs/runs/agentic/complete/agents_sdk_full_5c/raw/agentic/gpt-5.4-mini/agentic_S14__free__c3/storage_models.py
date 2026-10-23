from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class UploadRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    body: Optional[bytes] = None
    body_path: Optional[str] = None


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
    size: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[str]
    etag: Optional[str]
    metadata: Dict[str, str]


@dataclass
class ListResponse:
    bucket: str
    prefix: str
    objects: List[Dict[str, Any]]


@dataclass
class OCRResult:
    bucket: str
    key: str
    text: str
    raw_blocks: List[Dict[str, Any]]


@dataclass
class TranslationResult:
    source_text: str
    target_language: str
    translated_text: str


@dataclass
class SummaryResult:
    source_text: str
    summary: str


@dataclass
class EmbeddingResult:
    bucket: str
    key: str
    vector: List[float]
    dimensions: int


def normalize_datetime(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def dataclass_to_dict(instance: Any) -> Dict[str, Any]:
    return asdict(instance)


def normalize_s3_list(items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        normalized.append(
            {
                "key": item.get("Key"),
                "size": item.get("Size"),
                "etag": item.get("ETag"),
                "last_modified": normalize_datetime(item.get("LastModified")),
                "storage_class": item.get("StorageClass"),
            }
        )
    return normalized
