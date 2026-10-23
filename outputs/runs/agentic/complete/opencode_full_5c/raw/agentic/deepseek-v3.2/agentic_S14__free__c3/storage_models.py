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
    """Response from uploading an object."""

    success: bool
    object_key: str
    bucket: str
    s3_url: Optional[str] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    """Request for creating a presigned download URL."""

    bucket: str
    object_key: str
    expiration_seconds: Optional[int] = None


@dataclass
class PresignedUrlResponse:
    """Response containing a presigned URL."""

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
    """Response containing object metadata."""

    success: bool
    object_key: str
    bucket: str
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class ListRequest:
    """Request for listing objects with a prefix."""

    bucket: str
    prefix: Optional[str] = None
    max_keys: Optional[int] = None


@dataclass
class ObjectInfo:
    """Information about a stored object."""

    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str


@dataclass
class ListResponse:
    """Response containing a list of objects."""

    success: bool
    objects: List[ObjectInfo]
    bucket: str
    prefix: str
    count: int = 0
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class OCRRequest:
    """Request for OCR processing on a stored document."""

    bucket: str
    object_key: str
    language_code: Optional[str] = None
    output_format: Optional[str] = None


@dataclass
class OCRResponse:
    """Response from OCR processing."""

    success: bool
    extracted_text: Optional[str] = None
    confidence: Optional[float] = None
    object_key: str
    bucket: str
    error_message: Optional[str] = None
    message: Optional[str] = None


@dataclass
class TranslateRequest:
    """Request for translating text."""

    text: str
    source_language: Optional[str] = None
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
    """Request for summarizing content."""

    text: str
    max_length: Optional[int] = None


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
    """Request for embedding text."""

    text: str
    model: Optional[str] = None


@dataclass
class EmbeddingResponse:
    """Response containing embeddings."""

    success: bool
    embedding: Optional[List[float]] = None
    model: Optional[str] = None
    dimensions: Optional[int] = None
    error_message: Optional[str] = None
    message: Optional[str] = None
