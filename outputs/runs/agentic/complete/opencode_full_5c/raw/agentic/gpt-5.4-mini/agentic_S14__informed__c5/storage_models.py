from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


def normalize_bytes(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    if hasattr(data, "read"):
        return data.read()
    return bytes(data)


def normalize_text(data: Any) -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode("utf-8", errors="replace")
    return str(data)


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): normalize_text(v) for k, v in metadata.items()}


def first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


@dataclass
class ObjectReference:
    bucket: str
    key: str


@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[Any] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListedObject:
    bucket: str
    key: str
    size: Optional[int] = None
    last_modified: Optional[Any] = None
    etag: Optional[str] = None


def as_dict(result: Any) -> Dict[str, Any]:
    if hasattr(result, "__dict__"):
        return dict(result.__dict__)
    return dict(result)
