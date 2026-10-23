from typing import Dict, Optional, TypedDict
from dataclasses import dataclass


class ObjectMetadata(TypedDict, total=False):
    name: str
    size: int
    content_type: str
    time_created: str
    updated: str
    md5_hash: str
    metadata: Dict[str, str]


@dataclass
class UploadRequest:
    object_name: str
    data: bytes
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    object_name: str
    public_url: Optional[str] = None
    size: Optional[int] = None


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_in_seconds: int


@dataclass
class ListPrefixResponse:
    objects: list[str]
    prefixes: list[str]