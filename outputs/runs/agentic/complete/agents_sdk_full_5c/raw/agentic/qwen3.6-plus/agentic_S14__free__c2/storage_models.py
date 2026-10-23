"""
Request, response, and normalization helpers for Managed Object Storage.

Provides data models and utility functions for working with S3 object operations.
"""

import hashlib
import mimetypes
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List, BinaryIO
from io import BytesIO

import boto3

UPLOAD_CHUNK_SIZE = 8 * 1024 * 1024  # 8 MB


@dataclass
class UploadRequest:
    """Parameters for uploading an object to S3."""
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    cache_control: Optional[str] = None
    storage_class: Optional[str] = None
    encryption: Optional[str] = "AES256"
    acl: Optional[str] = None


@dataclass
class UploadResponse:
    """Result of an S3 upload operation."""
    bucket: str
    key: str
    etag: str
    version_id: Optional[str] = None
    content_length: int = 0
    content_type: Optional[str] = None
    success: bool = False
    error_message: Optional[str] = None

    @classmethod
    def from_s3_response(cls, bucket: str, key: str, s3_response: Dict[str, Any], success: bool = True) -> "UploadResponse":
        return cls(
            bucket=bucket,
            key=key,
            etag=s3_response.get("ETag", "").strip('"'),
            version_id=s3_response.get("VersionId"),
            content_length=s3_response.get("ContentLength", 0),
            content_type=s3_response.get("ContentType"),
            success=success,
        )


@dataclass
class PresignedUrlRequest:
    """Parameters for generating a presigned download URL."""
    bucket: str
    key: str
    expiry_seconds: int = 3600
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    """Result of presigned URL generation."""
    url: str
    bucket: str
    key: str
    expires_at: datetime
    method: str = "GET"


@dataclass
class ObjectMetadataResponse:
    """Parsed head object metadata from S3."""
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None
    content_language: Optional[str] = None
    content_encoding: Optional[str] = None
    expires: Optional[datetime] = None
    cache_control: Optional[str] = None
    exists: bool = True

    @classmethod
    def from_s3_head(cls, bucket: str, key: str, head_response: Dict[str, Any]) -> "ObjectMetadataResponse":
        return cls(
            bucket=bucket,
            key=key,
            content_type=head_response.get("ContentType"),
            content_length=head_response.get("ContentLength", 0),
            last_modified=head_response.get("LastModified"),
            etag=head_response.get("ETag", "").strip('"'),
            storage_class=head_response.get("StorageClass"),
            version_id=head_response.get("VersionId"),
            metadata={k.lower(): v for k, v in head_response.get("Metadata", {}).items()},
            server_side_encryption=head_response.get("ServerSideEncryption"),
            content_language=head_response.get("ContentLanguage"),
            content_encoding=head_response.get("ContentEncoding"),
            expires=head_response.get("Expires"),
            cache_control=head_response.get("CacheControl"),
            exists=True,
        )

    @classmethod
    def not_found(cls, bucket: str, key: str) -> "ObjectMetadataResponse":
        return cls(
            bucket=bucket,
            key=key,
            exists=False,
        )


@dataclass
class ListPrefixRequest:
    """Parameters for listing objects under a prefix."""
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000
    start_after: Optional[str] = None


@dataclass
class ObjectSummary:
    """Summary information for a listed S3 object."""
    key: str
    size: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    owner: Optional[str] = None


@dataclass
class ListPrefixResponse:
    """Result of listing objects under a prefix."""
    bucket: str
    prefix: str
    objects: List[ObjectSummary] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0

    @classmethod
    def from_s3_list(cls, bucket: str, prefix: str, list_response: Dict[str, Any]) -> "ListPrefixResponse":
        objects = []
        for item in list_response.get("Contents", []):
            objects.append(ObjectSummary(
                key=item["Key"],
                size=item.get("Size", 0),
                last_modified=item.get("LastModified"),
                etag=item.get("ETag", "").strip('"'),
                storage_class=item.get("StorageClass"),
            ))
        common_prefixes = list_response.get("CommonPrefixes", [])
        prefix_list = [cp["Prefix"] for cp in common_prefixes]
        return cls(
            bucket=bucket,
            prefix=prefix,
            objects=objects,
            common_prefixes=prefix_list,
            is_truncated=list_response.get("IsTruncated", False),
            next_continuation_token=list_response.get("NextContinuationToken"),
            key_count=list_response.get("KeyCount", len(objects)),
        )


def detect_content_type(key: str, data: Optional[bytes] = None) -> str:
    """Detect content type from file extension or data."""
    content_type, _ = mimetypes.guess_type(key)
    if content_type:
        return content_type
    if data:
        if data[:4] == b'\x89PNG':
            return "image/png"
        if data[:2] == b'\xff\xd8':
            return "image/jpeg"
        if data[:5] == b'%PDF-':
            return "application/pdf"
    return "application/octet-stream"


def compute_md5_hash(data: bytes) -> str:
    """Compute MD5 hash of data for ETag verification."""
    return hashlib.md5(data).hexdigest()


def prepare_upload_body(content: Optional[bytes] = None, file_path: Optional[str] = None, stream: Optional[BinaryIO] = None) -> BinaryIO:
    """Prepare upload body from various input sources."""
    if content is not None:
        return BytesIO(content)
    if file_path is not None:
        return open(file_path, "rb")
    if stream is not None:
        return stream
    raise ValueError("Must provide content, file_path, or stream for upload")
