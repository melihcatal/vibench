from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


@dataclass
class UploadRequest:
    """Request for uploading an object to storage."""

    bucket: str
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    """Response from upload operation."""

    success: bool
    object_key: str
    bucket: str
    object_url: Optional[str] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    """Request for creating a presigned download URL."""

    bucket: str
    object_key: str
    expiration_seconds: int = 3600  # Default 1 hour


@dataclass
class PresignedUrlResponse:
    """Response with presigned URL."""

    success: bool
    presigned_url: Optional[str] = None
    object_key: str
    bucket: str
    expiration_seconds: Optional[int] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class MetadataRequest:
    """Request for object metadata."""

    bucket: str
    object_key: str


@dataclass
class MetadataResponse:
    """Response with object metadata."""

    success: bool
    object_key: str
    bucket: str
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class ListRequest:
    """Request for listing objects with prefix."""

    bucket: str
    prefix: Optional[str] = None
    max_keys: Optional[int] = None


@dataclass
class ObjectInfo:
    """Information about a stored object."""

    key: str
    size: int
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class ListResponse:
    """Response with list of objects."""

    success: bool
    bucket: str
    prefix: Optional[str] = None
    objects: List[ObjectInfo] = field(default_factory=list)
    total_count: int = 0
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class OCRRequest:
    """Request for OCR processing."""

    bucket: str
    object_key: str
    language_code: Optional[str] = "en"
    output_format: Optional[str] = "text"


@dataclass
class OCRResponse:
    """Response from OCR processing."""

    success: bool
    object_key: str
    bucket: str
    extracted_text: Optional[str] = None
    confidence: Optional[float] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class TranslateRequest:
    """Request for text translation."""

    text: str
    source_language: Optional[str] = "auto"
    target_language: str = "en"


@dataclass
class TranslateResponse:
    """Response from translation."""

    success: bool
    translated_text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class SummaryRequest:
    """Request for content summarization."""

    text: str
    max_length: Optional[int] = 200
    language: Optional[str] = "en"


@dataclass
class SummaryResponse:
    """Response from summarization."""

    success: bool
    summary: Optional[str] = None
    original_length: Optional[int] = None
    summary_length: Optional[int] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class EmbeddingRequest:
    """Request for embedding generation."""

    text: str
    model: Optional[str] = "text-embedding-ada-002"


@dataclass
class EmbeddingResponse:
    """Response with embedding vector."""

    success: bool
    embedding: Optional[List[float]] = None
    model: Optional[str] = None
    dimensions: Optional[int] = None
    error_message: Optional[str] = None
    message: Optional[str] = None
