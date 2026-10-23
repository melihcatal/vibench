from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class StorageObject:
    """Represents a stored object in managed storage."""

    bucket: str
    key: str
    size: int
    etag: str
    last_modified: Optional[datetime] = None
    content_type: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    @property
    def s3_uri(self) -> str:
        """Get S3 URI for this object."""
        return f"s3://{self.bucket}/{self.key}"

    @property
    def is_directory(self) -> bool:
        """Check if object represents a directory (ends with /)."""
        return self.key.endswith("/")


@dataclass
class UploadRequest:
    """Request for uploading an object."""

    bucket: str
    key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def validate(self) -> bool:
        """Validate upload request."""
        if not self.bucket or not self.key:
            return False
        if not self.file_path and self.data is None:
            return False
        if self.file_path and self.data is not None:
            return False
        return True


@dataclass
class UploadResult:
    """Result of an upload operation."""

    success: bool
    bucket: str
    key: str
    etag: Optional[str] = None
    size: Optional[int] = None
    error: Optional[str] = None


@dataclass
class ListRequest:
    """Request for listing objects."""

    bucket: str
    prefix: str = ""
    max_keys: int = 1000
    continuation_token: Optional[str] = None

    def validate(self) -> bool:
        """Validate list request."""
        return bool(self.bucket)


@dataclass
class ListResult:
    """Result of a list operation."""

    success: bool
    bucket: str
    prefix: str
    objects: List[StorageObject]
    count: int
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    error: Optional[str] = None


@dataclass
class MetadataRequest:
    """Request for object metadata."""

    bucket: str
    key: str

    def validate(self) -> bool:
        """Validate metadata request."""
        return bool(self.bucket and self.key)


@dataclass
class MetadataResult:
    """Result of metadata operation."""

    success: bool
    bucket: str
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    error: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    """Request for presigned URL."""

    bucket: str
    key: str
    expiration_seconds: int = 3600
    operation: str = "get_object"  # 'get_object' or 'put_object'

    def validate(self) -> bool:
        """Validate presigned URL request."""
        if not self.bucket or not self.key:
            return False
        if self.expiration_seconds <= 0:
            return False
        if self.operation not in ["get_object", "put_object"]:
            return False
        return True


@dataclass
class PresignedUrlResult:
    """Result of presigned URL generation."""

    success: bool
    url: Optional[str] = None
    bucket: Optional[str] = None
    key: Optional[str] = None
    expiration: Optional[int] = None
    error: Optional[str] = None


def normalize_s3_response(response: Dict[str, Any]) -> StorageObject:
    """Normalize S3 API response to StorageObject."""
    return StorageObject(
        bucket=response.get("Bucket", ""),
        key=response.get("Key", ""),
        size=response.get("Size", 0),
        etag=response.get("ETag", ""),
        last_modified=response.get("LastModified"),
        content_type=response.get("ContentType"),
        storage_class=response.get("StorageClass", "STANDARD"),
        metadata=response.get("Metadata", {}),
    )
