from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StorageObjectRequest:
    bucket: str
    object_name: str
    data: Any = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class StorageObjectResponse:
    bucket: str
    object_name: str
    uri: str
    etag: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


def normalize_prefix(prefix: Optional[str]) -> str:
    if not prefix:
        return ""
    return prefix.lstrip("/")


def normalize_object_name(name: str) -> str:
    return name.lstrip("/")


def normalize_object_names(items: Iterable[Any]) -> List[str]:
    return [str(item) for item in items]
