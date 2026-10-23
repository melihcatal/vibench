from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class UploadResult:
    container: str
    blob: str
    etag: Optional[str] = None
    url: Optional[str] = None


@dataclass
class MetadataResult:
    container: str
    blob: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListingResult:
    container: str
    prefix: str
    objects: List[Dict[str, Any]]


def normalize_payload(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if hasattr(data, "read"):
        value = data.read()
        return value if isinstance(value, bytes) else str(value).encode("utf-8")
    return str(data).encode("utf-8")


def normalize_list_items(items: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items:
        normalized.append({
            "name": getattr(item, "name", None),
            "size": getattr(item, "size", None),
            "etag": getattr(item, "etag", None),
            "last_modified": str(getattr(item, "last_modified", None)) if getattr(item, "last_modified", None) else None,
        })
    return normalized
