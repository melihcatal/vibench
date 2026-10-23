from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(slots=True)
class StorageObjectRef:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass(slots=True)
class UploadPayload:
    bucket: str
    key: str
    body: bytes | str
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    def as_bytes(self) -> bytes:
        return self.body if isinstance(self.body, bytes) else self.body.encode("utf-8")


@dataclass(slots=True)
class ObjectMetadata:
    bucket: str
    key: str
    size: int
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ListedObject:
    key: str
    size: int | None = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass(slots=True)
class ListPrefixResult:
    bucket: str
    prefix: str
    objects: List[ListedObject] = field(default_factory=list)
    is_truncated: bool = False
    next_token: Optional[str] = None


@dataclass(slots=True)
class DocumentTextResult:
    source: StorageObjectRef
    text: str
    language: Optional[str] = None
    pages: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    provider: str = "google-translate"


@dataclass(slots=True)
class AssetSummaryResult:
    source: StorageObjectRef
    summary: str
    provider: str
    tags: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    source: StorageObjectRef
    vector: List[float]
    dimensions: int
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_metadata(metadata: Mapping[str, Any] | None) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not metadata:
        return out
    for key, value in metadata.items():
        if value is None:
            continue
        out[str(key).lower()] = str(value)
    return out


def coerce_text(parts: Iterable[Any]) -> str:
    return "\n".join(str(part).strip() for part in parts if str(part).strip())
