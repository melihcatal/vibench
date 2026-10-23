from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _to_dict(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _to_dict(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_dict(v) for v in value]
    return value


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): "" if v is None else str(v) for k, v in metadata.items()}


def normalize_bytes(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if hasattr(data, "read"):
        raw = data.read()
        return raw if isinstance(raw, bytes) else str(raw).encode("utf-8")
    return str(data).encode("utf-8")


@dataclass
class UploadRequest:
    bucket: str
    object_name: str
    body: Any
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UploadResponse:
    bucket: str
    object_name: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HeadObjectResponse:
    bucket: str
    object_name: str
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ListObjectsResponse:
    bucket: str
    prefix: str
    objects: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignedUrlResponse:
    bucket: str
    object_name: str
    url: str
    expires_in: int
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OcrResponse:
    bucket: str
    object_name: str
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResponse:
    source_language: str
    target_language: str
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SummaryResponse:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResponse:
    vector: List[float]
    dimensions: int
    raw: Dict[str, Any] = field(default_factory=dict)
