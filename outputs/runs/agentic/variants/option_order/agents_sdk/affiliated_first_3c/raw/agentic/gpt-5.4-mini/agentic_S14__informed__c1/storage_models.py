from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(frozen=True)
class ObjectReference:
    bucket: str
    name: str


@dataclass(frozen=True)
class UploadRequest:
    bucket: str
    name: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class ObjectMetadata:
    bucket: str
    name: str
    size: Optional[int]
    content_type: Optional[str]
    md5_hash: Optional[str]
    etag: Optional[str]
    metadata: Dict[str, str]
    updated: Optional[str]


@dataclass(frozen=True)
class ObjectListItem:
    bucket: str
    name: str
    size: Optional[int]
    updated: Optional[str]


@dataclass(frozen=True)
class NormalizedText:
    text: str
    language: Optional[str] = None
    source: Optional[str] = None


def normalize_metadata(meta: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not meta:
        return {}
    return {str(k): str(v) for k, v in meta.items() if v is not None}


def normalize_items(items: Iterable[Any]) -> List[ObjectListItem]:
    normalized: List[ObjectListItem] = []
    for item in items:
        normalized.append(
            ObjectListItem(
                bucket=getattr(item, "bucket", ""),
                name=getattr(item, "name", ""),
                size=getattr(item, "size", None),
                updated=str(getattr(item, "updated", None)) if getattr(item, "updated", None) else None,
            )
        )
    return normalized
