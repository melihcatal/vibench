from dataclasses import dataclass
from typing import Any, Mapping, Optional


def normalize_object_key(key: str) -> str:
    return key.lstrip('/')


def normalize_prefix(prefix: str) -> str:
    prefix = prefix.lstrip('/')
    return prefix if not prefix or prefix.endswith('/') else prefix + '/'


@dataclass
class StorageObjectRequest:
    bucket: str
    object_key: str
    content_type: Optional[str] = None
    metadata: Optional[Mapping[str, str]] = None


@dataclass
class StorageObjectResponse:
    bucket: str
    object_key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[Mapping[str, Any]] = None
