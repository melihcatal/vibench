from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict, Iterable, Optional, Union


BytesLike = Union[bytes, bytearray, memoryview]
BodyLike = Union[str, BytesLike, BytesIO]


def normalize_key(value: str) -> str:
    return value.lstrip("/")


def normalize_bucket(value: str) -> str:
    return value.strip()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): normalize_text(v) for k, v in metadata.items()}


def body_to_bytes(body: BodyLike) -> bytes:
    if isinstance(body, str):
        return body.encode("utf-8")
    if isinstance(body, (bytes, bytearray, memoryview)):
        return bytes(body)
    if hasattr(body, "read"):
        data = body.read()
        return data if isinstance(data, bytes) else normalize_text(data).encode("utf-8")
    return normalize_text(body).encode("utf-8")


@dataclass
class StorageObjectInfo:
    bucket: str
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class StorageListResult:
    bucket: str
    prefix: str
    objects: Iterable[StorageObjectInfo]
