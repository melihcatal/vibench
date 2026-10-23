from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_object_name(name: str) -> str:
    return name.strip().lstrip("/")


def normalize_prefix(prefix: Optional[str]) -> str:
    if not prefix:
        return ""
    return prefix.strip().lstrip("/")


@dataclass
class StorageUploadRequest:
    bucket: str
    object_name: str
    content: Any
    content_type: Optional[str] = None


@dataclass
class StorageObjectRef:
    bucket: str
    object_name: str


@dataclass
class StorageListRequest:
    bucket: str
    prefix: str = ""


@dataclass
class StorageMetadataResponse:
    bucket: str
    object_name: str
    metadata: Dict[str, Any]
