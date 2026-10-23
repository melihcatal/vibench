from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class StorageObject:
    """Represents an object in managed storage."""

    bucket: str
    key: str
    size: int
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    metadata: Dict[str, str] = None
    provider: str = "Amazon S3"

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class UploadRequest:
    """Request for uploading an object."""

    bucket: str
    key: str
    file_path: Optional[str] = None
    data_bytes: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.file_path and not self.data_bytes:
            raise ValueError("Either file_path or data_bytes must be provided")


@dataclass
class UploadResult:
    """Result of an upload operation."""

    bucket: str
    key: str
    etag: str
    provider: str
    size: Optional[int] = None


@dataclass
class ListRequest:
    """Request for listing objects."""

    bucket: str
    prefix: str = ""
    max_keys: int = 1000


@dataclass
class ListResult:
    """Result of a list operation."""

    bucket: str
    prefix: str
    objects: List[StorageObject]
    count: int
    provider: str


@dataclass
class PresignedUrlRequest:
    """Request for generating a presigned URL."""

    bucket: str
    key: str
    expiration_seconds: int = 3600


def normalize_metadata(raw_metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Normalize metadata values to strings.

    Args:
        raw_metadata: Raw metadata dictionary

    Returns:
        Dict[str, str]: Normalized metadata with string values
    """
    normalized = {}
    for key, value in raw_metadata.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (int, float, bool)):
            normalized[key] = str(value)
        elif isinstance(value, str):
            normalized[key] = value
        else:
            normalized[key] = str(value)
    return normalized


def storage_object_from_s3_response(
    s3_response: Dict[str, Any], bucket: str, key: str
) -> StorageObject:
    """
    Create StorageObject from S3 response.

    Args:
        s3_response: S3 API response
        bucket: Bucket name
        key: Object key

    Returns:
        StorageObject: Normalized storage object
    """
    return StorageObject(
        bucket=bucket,
        key=key,
        size=s3_response.get("ContentLength", 0),
        content_type=s3_response.get("ContentType"),
        last_modified=s3_response.get("LastModified", datetime.utcnow()).isoformat()
        if s3_response.get("LastModified")
        else None,
        etag=s3_response.get("ETag"),
        metadata=normalize_metadata(s3_response.get("Metadata", {})),
        provider="Amazon S3",
    )
