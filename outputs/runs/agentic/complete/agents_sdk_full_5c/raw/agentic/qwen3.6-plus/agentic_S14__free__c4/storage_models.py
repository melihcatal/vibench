"""Define local request, response, and normalization helpers for Managed Object Storage."""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
import hashlib


@dataclass
class UploadRequest:
    """Request model for uploading an object to S3."""
    bucket: str
    key: str
    content: bytes = field(repr=False)
    content_type: str = "application/octet-stream"
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    server_side_encryption: Optional[str] = None

    def to_boto_kwargs(self) -> dict:
        """Convert to kwargs suitable for boto3 put_object."""
        kwargs = {
            "Bucket": self.bucket,
            "Key": self.key,
            "Body": self.content,
            "ContentType": self.content_type,
            "StorageClass": self.storage_class,
        }
        if self.metadata:
            kwargs["Metadata"] = self.metadata
        if self.server_side_encryption:
            kwargs["ServerSideEncryption"] = self.server_side_encryption
        return kwargs


@dataclass
class UploadResponse:
    """Response model after a successful upload."""
    object_key: str
    bucket: str
    etag: str
    version_id: Optional[str] = None
    content_length: int = 0
    storage_class: Optional[str] = None

    @classmethod
    def from_boto_response(cls, key: str, bucket: str, response: dict, content: bytes) -> "UploadResponse":
        return cls(
            object_key=key,
            bucket=bucket,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            content_length=len(content),
            storage_class=response.get("StorageClass"),
        )


@dataclass
class PresignedUrlRequest:
    """Request model for generating a presigned download URL."""
    bucket: str
    key: str
    expiration_seconds: int = 3600
    http_method: str = "GET"


@dataclass
class PresignedUrlResponse:
    """Response model containing the presigned URL."""
    url: str
    key: str
    bucket: str
    expires_in: int
    http_method: str


@dataclass
class ObjectMetadata:
    """Normalized object metadata from S3 HEAD request."""
    key: str
    bucket: str
    content_type: Optional[str] = None
    content_length: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    user_metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None

    @classmethod
    def from_head_response(cls, key: str, bucket: str, head_response: dict) -> "ObjectMetadata":
        return cls(
            key=key,
            bucket=bucket,
            content_type=head_response.get("ContentType"),
            content_length=int(head_response.get("ContentLength", 0)),
            etag=head_response.get("ETag", "").strip('"'),
            last_modified=head_response.get("LastModified"),
            storage_class=head_response.get("StorageClass"),
            user_metadata=head_response.get("Metadata", {}),
            version_id=head_response.get("VersionId"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        data = asdict(self)
        if data["last_modified"] and isinstance(data["last_modified"], datetime):
            data["last_modified"] = data["last_modified"].isoformat()
        return data


@dataclass
class ListedObject:
    """Normalized representation of an object returned from a list operation."""
    key: str
    size: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None

    @classmethod
    def from_s3_object(cls, s3_obj: dict) -> "ListedObject":
        return cls(
            key=s3_obj.get("Key", ""),
            size=s3_obj.get("Size", 0),
            last_modified=s3_obj.get("LastModified"),
            etag=s3_obj.get("ETag", "").strip('"'),
            storage_class=s3_obj.get("StorageClass"),
        )


@dataclass
class ListPrefixRequest:
    """Request model for listing objects under a prefix."""
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000
    continuation_token: Optional[str] = None


@dataclass
class ListPrefixResponse:
    """Response model for prefix listing."""
    objects: List[ListedObject] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0


@dataclass
class OCRTaskRequest:
    """Request model for OCR via AWS Textract."""
    bucket: str
    key: str
    document_type: str = "application/pdf"


@dataclass
class OCRResult:
    """Normalized OCR result from AWS Textract."""
    text: str = ""
    confidence: float = 0.0
    pages: int = 0
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranslationRequest:
    """Request model for AWS Translate."""
    text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslationResult:
    """Normalized translation result."""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    character_count: int = 0


@dataclass
class SummaryRequest:
    """Request model for summarization via Bedrock."""
    text: str
    max_tokens: int = 512
    temperature: float = 0.3


@dataclass
class SummaryResult:
    """Normalized summary result."""
    summary: str = ""
    model_id: str = ""
    token_usage: Dict[str, int] = field(default_factory=dict)


@dataclass
class EmbeddingRequest:
    """Request model for embedding via Bedrock."""
    text: str
    model_id: str = "amazon.titan-embed-text-v1"


@dataclass
class EmbeddingResult:
    """Normalized embedding result."""
    vector: List[float] = field(default_factory=list)
    model_id: str = ""
    input_token_count: int = 0
