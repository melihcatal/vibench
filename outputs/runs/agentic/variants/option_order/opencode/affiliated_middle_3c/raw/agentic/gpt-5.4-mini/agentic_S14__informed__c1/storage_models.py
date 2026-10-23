from dataclasses import dataclass
from typing import Any


def normalize_prefix(prefix: str | None) -> str:
    if not prefix:
        return ""
    return prefix.lstrip("/")


def normalize_key(key: str) -> str:
    return key.lstrip("/")


@dataclass
class ObjectUploadResult:
    bucket: str
    key: str
    etag: str | None = None


@dataclass
class ObjectMetadataResult:
    bucket: str
    key: str
    metadata: dict[str, Any]


@dataclass
class ListObjectsResult:
    bucket: str
    prefix: str
    keys: list[str]
