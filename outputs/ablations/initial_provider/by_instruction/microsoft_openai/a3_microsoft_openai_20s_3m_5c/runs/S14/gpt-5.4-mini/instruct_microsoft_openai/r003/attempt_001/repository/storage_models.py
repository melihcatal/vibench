from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class UploadRequest:
    container_name: str
    object_name: str
    content: Any
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class StorageObjectInfo:
    container_name: str
    object_name: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class SignedUrlRequest:
    container_name: str
    object_name: str
    expires_in_seconds: int = 3600


@dataclass
class OCRResult:
    text: str
    language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class SummaryResult:
    source_text: str
    summary: str
    raw: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    text: str
    embedding: Any
    raw: Optional[Dict[str, Any]] = None
