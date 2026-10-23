from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StorageObjectRequest:
    bucket: str
    key: str
    body: Any = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class StorageObjectInfo:
    bucket: str
    key: str
    etag: Optional[str] = None
    size: Optional[int] = None
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class StorageListResult:
    bucket: str
    prefix: str
    keys: List[str]


def normalize_key(value: str) -> str:
    return value.lstrip("/")


def normalize_prefix(value: Optional[str]) -> str:
    return "" if not value else value.lstrip("/")
