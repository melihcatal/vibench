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
    metadata: Optional[Dict[str, str]] = None
    content_type: Optional[str] = None


@dataclass
class UploadResponse:
    """Response from upload operation."""

    success: bool
    object_url: Optional[str] = None
    bucket: Optional[str] = None
    object_key: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    """Request for creating a presigned URL."""

    bucket: str
    object_key: str
    expiration_seconds: Optional[int] = None


@dataclass
class PresignedUrlResponse:
    """Response with presigned URL."""

    success: bool
    presigned_url: Optional[str] = None
    bucket: Optional[str] = None
    object_key: Optional[str] = None
    expiration_seconds: Optional[int] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class MetadataRequest:
    """Request for object metadata."""

    bucket: str
    object_key: str


@dataclass
class MetadataResponse:
    """Response with object metadata."""

    success: bool
    metadata: Optional[Dict[str, Any]] = None
    bucket: Optional[str] = None
    object_key: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class ListRequest:
    """Request for listing objects."""

    bucket: str
    prefix: Optional[str] = None
    max_keys: Optional[int] = None


@dataclass
class S3Object:
    """Represents an S3 object."""

    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str = "STANDARD"


@dataclass
class ListResponse:
    """Response from list operation."""

    success: bool
    objects: List[S3Object] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    bucket: Optional[str] = None
    prefix: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class OCRRequest:
    """Request for OCR processing."""

    bucket: str
    object_key: str
    language_code: Optional[str] = "en"
    output_bucket: Optional[str] = None
    output_prefix: Optional[str] = None


@dataclass
class OCRResponse:
    """Response from OCR processing."""

    success: bool
    extracted_text: Optional[str] = None
    confidence: Optional[float] = None
    bucket: Optional[str] = None
    object_key: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class TranslationRequest:
    """Request for text translation."""

    text: str
    source_language_code: Optional[str] = "auto"
    target_language_code: str = "en"


@dataclass
class TranslationResponse:
    """Response from translation."""

    success: bool
    translated_text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class SummaryRequest:
    """Request for content summarization."""

    text: str
    max_length: Optional[int] = 150
    min_length: Optional[int] = 30


@dataclass
class SummaryResponse:
    """Response from summarization."""

    success: bool
    summary: Optional[str] = None
    original_length: Optional[int] = None
    summary_length: Optional[int] = None
    message: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class EmbeddingRequest:
    """Request for embedding generation."""

    text: str
    model: Optional[str] = "text-embedding-ada-002"


@dataclass
class EmbeddingResponse:
    """Response with embedding."""

    success: bool
    embedding: Optional[List[float]] = None
    model: Optional[str] = None
    dimensions: Optional[int] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
