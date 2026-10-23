from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ObjectKey:
    bucket: str
    key: str


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: Any
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class DownloadUrlRequest:
    bucket: str
    key: str
    expires_in: int = 3600


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    etag: Optional[str] = None
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListedObject:
    bucket: str
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    max_items: Optional[int] = None


@dataclass
class NormalizedResult:
    data: Dict[str, Any]


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    if not metadata:
        return normalized
    for key, value in metadata.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def to_dict(dataclass_value: Any) -> Dict[str, Any]:
    return asdict(dataclass_value)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def join_text(chunks: Iterable[Any]) -> str:
    return "\n".join(normalize_text(chunk) for chunk in chunks if normalize_text(chunk))
