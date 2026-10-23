from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Union


def normalize_bytes(data: Union[str, bytes, bytearray, memoryview, Iterable[int]]) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    if isinstance(data, str):
        return data.encode("utf-8")
    return bytes(data)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


@dataclass
class UploadRequest:
    bucket: str
    key: str
    data: Any
    content_type: Optional[str] = None


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    generation: Optional[str] = None


@dataclass
class DownloadUrlResponse:
    bucket: str
    key: str
    url: str
    expires_in: int


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    updated: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class ListObjectsResponse:
    bucket: str
    prefix: str
    objects: List[Dict[str, Any]]


@dataclass
class OcrResult:
    bucket: str
    key: str
    text: str
    provider: str = "google"


@dataclass
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    text: str


@dataclass
class SummaryResult:
    text: str


@dataclass
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    provider: str
