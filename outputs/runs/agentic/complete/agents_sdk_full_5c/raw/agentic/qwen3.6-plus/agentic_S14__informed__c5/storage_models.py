"""
storage_models.py - Define local request, response, and normalization helpers for Managed Object Storage.

Provides dataclasses and helper functions for normalizing S3 object storage responses
into consistent internal representations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class StorageUploadRequest:
    """Request model for uploading an object to managed storage."""

    bucket_name: str
    object_key: str
    content: Optional[bytes] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"


@dataclass
class StorageUploadResponse:
    """Response model for a successful object upload."""

    success: bool
    bucket_name: str
    object_key: str
    version_id: Optional[str] = None
    etag: Optional[str] = None
    request_id: Optional[str] = None


@dataclass
class StorageObjectMetadata:
    """Normalized metadata for a stored object."""

    bucket_name: str
    object_key: str
    content_length: int
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    user_metadata: Dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None


@dataclass
class StorageObjectListing:
    """Normalized listing of objects under a prefix."""

    bucket_name: str
    prefix: str
    objects: List[StorageObjectMetadata] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    """Response model for a presigned URL generation."""

    url: str
    bucket_name: str
    object_key: str
    expires_in_seconds: int
    http_method: str = "GET"


def normalize_s3_head_response(
    head_response: Dict[str, Any], bucket_name: str, object_key: str
) -> StorageObjectMetadata:
    """
    Normalize a boto3 S3 head_object response into a StorageObjectMetadata instance.

    Args:
        head_response: Raw dict from boto3 head_object call.
        bucket_name: S3 bucket name.
        object_key: S3 object key.

    Returns:
        Normalized StorageObjectMetadata.
    """
    return StorageObjectMetadata(
        bucket_name=bucket_name,
        object_key=object_key,
        content_length=head_response.get("ContentLength", 0),
        content_type=head_response.get("ContentType"),
        etag=head_response.get("ETag", "").strip('"'),
        last_modified=head_response.get("LastModified"),
        storage_class=head_response.get("StorageClass"),
        version_id=head_response.get("VersionId"),
        user_metadata={
            k[len("x-amz-meta-") :]: v
            for k, v in head_response.get("Metadata", {}).items()
        },
        server_side_encryption=head_response.get("ServerSideEncryption"),
    )


def normalize_s3_list_response(
    list_response: Dict[str, Any], bucket_name: str, prefix: str
) -> StorageObjectListing:
    """
    Normalize a boto3 S3 list_objects_v2 response into a StorageObjectListing.

    Args:
        list_response: Raw dict from boto3 list_objects_v2 call.
        bucket_name: S3 bucket name.
        prefix: S3 object prefix.

    Returns:
        Normalized StorageObjectListing.
    """
    objects = []
    for item in list_response.get("Contents", []):
        metadata = StorageObjectMetadata(
            bucket_name=bucket_name,
            object_key=item["Key"],
            content_length=item.get("Size", 0),
            etag=item.get("ETag", "").strip('"'),
            last_modified=item.get("LastModified"),
            storage_class=item.get("StorageClass"),
        )
        objects.append(metadata)

    common_prefixes = [
        cp["Prefix"] for cp in list_response.get("CommonPrefixes", [])
    ]

    return StorageObjectListing(
        bucket_name=bucket_name,
        prefix=prefix,
        objects=objects,
        common_prefixes=common_prefixes,
        is_truncated=list_response.get("IsTruncated", False),
        next_continuation_token=list_response.get("NextContinuationToken"),
    )
