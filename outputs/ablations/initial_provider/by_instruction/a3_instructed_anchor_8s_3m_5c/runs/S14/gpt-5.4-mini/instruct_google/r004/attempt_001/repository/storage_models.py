from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_object_name(value: str) -> str:
    return value.lstrip("/")


def normalize_prefix(value: Optional[str]) -> str:
    return "" if value in (None, "") else value.lstrip("/")


@dataclass
class StorageObjectRef:
    bucket: str
    name: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UploadResult:
    bucket: str
    name: str
    content_type: Optional[str] = None
    size: Optional[int] = None
    md5_hash: Optional[str] = None
    generation: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ObjectMetadata:
    bucket: str
    name: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    md5_hash: Optional[str] = None
    crc32c: Optional[str] = None
    updated: Optional[str] = None
    etag: Optional[str] = None
    generation: Optional[int] = None
    metadata: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ListedObject:
    bucket: str
    name: str
    size: Optional[int] = None
    updated: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SignedUrlResult:
    url: str
    bucket: str
    name: str
    expires_in: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentInsight:
    bucket: str
    name: str
    text: Optional[str] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    translated_text: Optional[str] = None
    embedding: Optional[list] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
