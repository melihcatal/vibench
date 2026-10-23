"""
Local request, response, and normalization helpers for Managed Object Storage.

Provides dataclasses and helpers for normalizing S3 responses and
representing object metadata, upload results, and listing entries.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class UploadResult:
    """Normalized result after uploading an object to S3."""
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_length: int = 0
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    success: bool = True

    @classmethod
    def from_s3_response(cls, bucket: str, key: str, response: Dict[str, Any]) -> "UploadResult":
        """Normalize a boto3 put_object response."""
        return cls(
            bucket=bucket,
            key=key,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            content_length=int(response.get("ContentLength", 0)),
            storage_class=response.get("StorageClass"),
            metadata=response.get("Metadata", {}),
            success=True,
        )


@dataclass
class ObjectMetadata:
    """Normalized metadata for a stored S3 object."""
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    exists: bool = True

    @classmethod
    def from_s3_head(cls, bucket: str, key: str, response: Dict[str, Any]) -> "ObjectMetadata":
        """Normalize a boto3 head_object response."""
        return cls(
            bucket=bucket,
            key=key,
            content_type=response.get("ContentType"),
            content_length=int(response.get("ContentLength", 0)),
            last_modified=response.get("LastModified"),
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            storage_class=response.get("StorageClass"),
            metadata=response.get("Metadata", {}),
            exists=True,
        )


@dataclass
class ObjectListing:
    """Normalized listing entry for objects under a prefix."""
    bucket: str
    key: str
    size: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    is_prefix: bool = False

    @classmethod
    def from_s3_object(cls, bucket: str, obj: Dict[str, Any], is_prefix: bool = False) -> "ObjectListing":
        """Normalize an S3 list_objects_v2 entry."""
        return cls(
            bucket=bucket,
            key=obj.get("Key", ""),
            size=int(obj.get("Size", 0)),
            last_modified=obj.get("LastModified"),
            etag=obj.get("ETag", "").strip('"') if obj.get("ETag") else None,
            storage_class=obj.get("StorageClass"),
            is_prefix=is_prefix,
        )


@dataclass
class PresignedUrlResult:
    """Result containing a presigned download URL."""
    url: str
    bucket: str
    key: str
    expires_in_seconds: int = 3600
    http_method: str = "GET"
