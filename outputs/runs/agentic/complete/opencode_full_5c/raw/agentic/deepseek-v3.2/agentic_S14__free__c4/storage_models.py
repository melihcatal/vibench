from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class UploadRequest:
    """Request model for uploading objects to storage."""

    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: str = "application/octet-stream"
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class UploadResponse:
    """Response model for upload operations."""

    success: bool
    bucket: Optional[str] = None
    key: Optional[str] = None
    url: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    """Request model for generating presigned URLs."""

    bucket: str
    key: str
    expiration_seconds: int = 3600
    operation: str = "get_object"  # "get_object" or "put_object"
    content_type: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    """Response model for presigned URL operations."""

    success: bool
    url: Optional[str] = None
    bucket: Optional[str] = None
    key: Optional[str] = None
    expiration_seconds: Optional[int] = None
    expiration_time: Optional[str] = None
    content_type: Optional[str] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class ObjectMetadataRequest:
    """Request model for retrieving object metadata."""

    bucket: str
    key: str


@dataclass
class ObjectMetadataResponse:
    """Response model for object metadata operations."""

    success: bool
    bucket: Optional[str] = None
    key: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None
    kms_key_id: Optional[str] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class ListObjectsRequest:
    """Request model for listing objects."""

    bucket: str
    prefix: str = ""
    max_keys: int = 1000
    delimiter: Optional[str] = None


@dataclass
class S3Object:
    """Model representing an S3 object."""

    key: str
    size: int
    last_modified: str
    etag: str
    storage_class: str = "STANDARD"


@dataclass
class ListObjectsResponse:
    """Response model for list objects operations."""

    success: bool
    bucket: Optional[str] = None
    prefix: Optional[str] = None
    objects: List[S3Object] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    continuation_token: Optional[str] = None
    max_keys: Optional[int] = None
    key_count: Optional[int] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class OCRRequest:
    """Request model for OCR operations."""

    bucket: str
    key: str
    language_code: str = "en"
    output_bucket: Optional[str] = None
    output_prefix: Optional[str] = None


@dataclass
class OCRResponse:
    """Response model for OCR operations."""

    success: bool
    text: Optional[str] = None
    confidence: Optional[float] = None
    pages: Optional[int] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class TranslateRequest:
    """Request model for translation operations."""

    text: str
    source_language_code: str = "auto"
    target_language_code: str = "en"


@dataclass
class TranslateResponse:
    """Response model for translation operations."""

    success: bool
    translated_text: Optional[str] = None
    source_language_code: Optional[str] = None
    target_language_code: Optional[str] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class SummaryRequest:
    """Request model for content summarization."""

    text: str
    max_length: int = 200
    min_length: int = 50


@dataclass
class SummaryResponse:
    """Response model for summarization operations."""

    success: bool
    summary: Optional[str] = None
    original_length: Optional[int] = None
    summary_length: Optional[int] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class EmbeddingRequest:
    """Request model for embedding operations."""

    text: str
    model: str = "text-embedding-ada-002"


@dataclass
class EmbeddingResponse:
    """Response model for embedding operations."""

    success: bool
    embedding: Optional[List[float]] = None
    model: Optional[str] = None
    dimensions: Optional[int] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None


@dataclass
class AssetMetadata:
    """Model for asset metadata with embeddings."""

    bucket: str
    key: str
    content_type: str
    size: int
    last_modified: str
    extracted_text: Optional[str] = None
    summary: Optional[str] = None
    language: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_s3_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize S3 API response to a standard format.

    Args:
        response: Raw S3 API response

    Returns:
        Normalized response dictionary
    """
    normalized = {}

    if "ResponseMetadata" in response:
        normalized["request_id"] = response["ResponseMetadata"].get("RequestId")
        normalized["http_status"] = response["ResponseMetadata"].get("HTTPStatusCode")

    # Copy relevant fields
    for key in [
        "Bucket",
        "Key",
        "Size",
        "ContentType",
        "ETag",
        "LastModified",
        "StorageClass",
    ]:
        if key in response:
            normalized[key.lower()] = response[key]

    # Handle metadata
    if "Metadata" in response:
        normalized["metadata"] = response["Metadata"]

    # Handle encryption
    if "ServerSideEncryption" in response:
        normalized["server_side_encryption"] = response["ServerSideEncryption"]

    if "SSEKMSKeyId" in response:
        normalized["kms_key_id"] = response["SSEKMSKeyId"]

    return normalized


def create_error_response(error: Exception, provider: str = "aws_s3") -> Dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        error: Exception that occurred
        provider: Service provider name

    Returns:
        Standardized error response
    """
    return {
        "success": False,
        "error_message": str(error),
        "error_type": type(error).__name__,
        "provider": provider,
    }
