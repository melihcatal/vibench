from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class StorageConfig:
    """Storage configuration model."""

    provider: str
    bucket_name: str
    region: str
    access_key_id: str
    secret_access_key: str
    endpoint_url: Optional[str] = None


@dataclass
class UploadRequest:
    """Upload request model."""

    file_path: Optional[str]
    data_bytes: Optional[bytes]
    content_type: str
    metadata: Dict[str, str]


@dataclass
class ObjectMetadata:
    """Object metadata model."""

    content_length: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]
    etag: Optional[str]
    storage_class: str
    user_metadata: Dict[str, str]
    server_side_encryption: Optional[str]
    version_id: Optional[str]


@dataclass
class ListObjectsResult:
    """List objects result model."""

    bucket: str
    prefix: str
    objects: List[Dict[str, Any]]
    common_prefixes: List[str]
    is_truncated: bool
    continuation_token: Optional[str]


@dataclass
class PresignedUrlResult:
    """Presigned URL result model."""

    url: str
    bucket: str
    key: str
    expires_at: datetime
    method: str


@dataclass
class UploadResult:
    """Upload result model."""

    success: bool
    bucket: str
    key: str
    url: Optional[str]
    etag: Optional[str]
    version_id: Optional[str]
    error: Optional[str] = None


@dataclass
class OCRResult:
    """OCR result model."""

    text: str
    confidence: float
    pages: List[Dict[str, Any]]
    raw_response: Dict[str, Any]


@dataclass
class TranslationResult:
    """Translation result model."""

    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float


@dataclass
class SummaryResult:
    """Summary result model."""

    original_text: str
    summary: str
    model_id: str
    token_count: int


@dataclass
class EmbeddingResult:
    """Embedding result model."""

    text: str
    embedding: List[float]
    model_id: str
    dimensions: int
