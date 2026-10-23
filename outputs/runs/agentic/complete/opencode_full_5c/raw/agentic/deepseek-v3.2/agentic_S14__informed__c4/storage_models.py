from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List


@dataclass
class ObjectInfo:
    """Basic information about a stored object."""

    key: str
    size: int
    last_modified: datetime
    etag: str
    storage_class: str = "STANDARD"


@dataclass
class ObjectMetadata:
    """Detailed metadata for a stored object."""

    key: str
    bucket: str
    size: int
    content_type: str
    etag: str
    last_modified: Optional[datetime] = None
    version_id: Optional[str] = None
    storage_class: str = "STANDARD"
    metadata: Dict[str, str] = field(default_factory=dict)
    custom_headers: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UploadResult:
    """Result of an upload operation."""

    success: bool
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


@dataclass
class OCRResult:
    """Result of OCR processing."""

    success: bool
    text: Optional[str] = None
    pages: Optional[List[Dict[str, Any]]] = None
    confidence: Optional[float] = None
    error: Optional[str] = None


@dataclass
class TranslationResult:
    """Result of text translation."""

    success: bool
    translated_text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SummaryResult:
    """Result of content summarization."""

    success: bool
    summary: Optional[str] = None
    model_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class EmbeddingResult:
    """Result of text embedding."""

    success: bool
    embedding: Optional[List[float]] = None
    model_id: Optional[str] = None
    dimensions: Optional[int] = None
    error: Optional[str] = None


def normalize_s3_key(key: str) -> str:
    """
    Normalize S3 key by removing leading slash if present.

    Args:
        key: S3 object key

    Returns:
        Normalized key
    """
    if key.startswith("/"):
        return key[1:]
    return key


def parse_s3_uri(s3_uri: str) -> tuple[str, str]:
    """
    Parse S3 URI into bucket and key.

    Args:
        s3_uri: S3 URI in format s3://bucket/key

    Returns:
        Tuple of (bucket, key)
    """
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {s3_uri}. Must start with 's3://'")

    parts = s3_uri[5:].split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""

    return bucket, key


def build_s3_uri(bucket: str, key: str) -> str:
    """
    Build S3 URI from bucket and key.

    Args:
        bucket: S3 bucket name
        key: S3 object key

    Returns:
        S3 URI string
    """
    normalized_key = normalize_s3_key(key)
    return f"s3://{bucket}/{normalized_key}"
