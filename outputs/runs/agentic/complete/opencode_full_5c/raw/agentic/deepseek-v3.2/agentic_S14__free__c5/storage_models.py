from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


@dataclass
class UploadRequest:
    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    success: bool
    bucket: str
    key: str
    url: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expiration_seconds: int = 3600  # Default 1 hour


@dataclass
class PresignedUrlResponse:
    success: bool
    bucket: str
    key: str
    presigned_url: Optional[str] = None
    expiration_seconds: Optional[int] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class MetadataRequest:
    bucket: str
    key: str


@dataclass
class MetadataResponse:
    success: bool
    bucket: str
    key: str
    metadata: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class ListRequest:
    bucket: str
    prefix: Optional[str] = None
    max_keys: Optional[int] = None
    continuation_token: Optional[str] = None


@dataclass
class ObjectInfo:
    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str


@dataclass
class ListResponse:
    success: bool
    bucket: str
    prefix: Optional[str] = None
    objects: List[ObjectInfo] = None
    next_continuation_token: Optional[str] = None
    is_truncated: bool = False
    message: Optional[str] = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.objects is None:
            self.objects = []


@dataclass
class OCRRequest:
    bucket: str
    key: str
    language: Optional[str] = "en"
    output_format: Optional[str] = "text"


@dataclass
class OCRResponse:
    success: bool
    bucket: str
    key: str
    extracted_text: Optional[str] = None
    confidence: Optional[float] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = "auto"
    target_language: str = "en"


@dataclass
class TranslationResponse:
    success: bool
    original_text: str
    translated_text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class SummaryRequest:
    text: str
    max_length: Optional[int] = 150
    language: Optional[str] = "en"


@dataclass
class SummaryResponse:
    success: bool
    original_text: str
    summary: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    model: Optional[str] = "text-embedding-ada-002"


@dataclass
class EmbeddingResponse:
    success: bool
    text: str
    embedding: Optional[List[float]] = None
    model: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
