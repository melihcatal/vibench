"""
Local request, response, and normalization helpers for Amazon S3 Managed Object Storage.
"""

import hashlib
import mimetypes
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class UploadRequest:
    """Normalized upload request for S3 objects."""
    bucket: str
    object_key: str
    body: Any  # bytes or file-like object
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"

    def detect_content_type(self) -> str:
        """Detect content type from object key or default to binary."""
        if self.content_type:
            return self.content_type
        guessed, _ = mimetypes.guess_type(self.object_key)
        return guessed or "application/octet-stream"


@dataclass
class UploadResponse:
    """Normalized upload response from S3."""
    bucket: str
    object_key: str
    etag: str
    version_id: Optional[str] = None
    storage_class: str = "STANDARD"
    content_length: Optional[int] = None
    server_side_encryption: Optional[str] = None

    @classmethod
    def from_s3_response(cls, put_response: Dict, request: UploadRequest) -> "UploadResponse":
        """Create UploadResponse from boto3 put_object response."""
        return cls(
            bucket=request.bucket,
            object_key=request.object_key,
            etag=put_response.get("ETag", "").strip('"'),
            version_id=put_response.get("VersionId"),
            storage_class=request.storage_class,
            content_length=request.content_length,
            server_side_encryption=put_response.get("ServerSideEncryption"),
        )


@dataclass
class PresignedUrlRequest:
    """Normalized presigned URL generation request."""
    bucket: str
    object_key: str
    expiration_seconds: int = 3600
    http_method: str = "GET"


@dataclass
class PresignedUrlResponse:
    """Normalized presigned URL response."""
    url: str
    bucket: str
    object_key: str
    expires_at: datetime
    http_method: str = "GET"


@dataclass
class ObjectMetadataResponse:
    """Normalized object metadata/head response."""
    bucket: str
    object_key: str
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None
    version_id: Optional[str] = None
    cache_control: Optional[str] = None
    content_disposition: Optional[str] = None
    content_encoding: Optional[str] = None

    @classmethod
    def from_s3_head(cls, head_response: Dict, bucket: str, object_key: str) -> "ObjectMetadataResponse":
        """Create ObjectMetadataResponse from boto3 head_object response."""
        return cls(
            bucket=bucket,
            object_key=object_key,
            content_type=head_response.get("ContentType"),
            content_length=head_response.get("ContentLength"),
            etag=head_response.get("ETag", "").strip('"'),
            last_modified=head_response.get("LastModified"),
            storage_class=head_response.get("StorageClass"),
            metadata=head_response.get("Metadata", {}),
            server_side_encryption=head_response.get("ServerSideEncryption"),
            version_id=head_response.get("VersionId"),
            cache_control=head_response.get("CacheControl"),
            content_disposition=head_response.get("ContentDisposition"),
            content_encoding=head_response.get("ContentEncoding"),
        )


@dataclass
class ListPrefixResponse:
    """Normalized list objects under prefix response."""
    bucket: str
    prefix: str
    objects: List[Dict[str, Any]] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    max_keys: Optional[int] = None

    @classmethod
    def from_s3_list(cls, list_response: Dict, bucket: str, prefix: str) -> "ListPrefixResponse":
        """Create ListPrefixResponse from boto3 list_objects_v2 response."""
        objects = []
        for item in list_response.get("Contents", []):
            objects.append({
                "key": item["Key"],
                "size": item.get("Size"),
                "last_modified": item.get("LastModified"),
                "etag": item.get("ETag", "").strip('"'),
                "storage_class": item.get("StorageClass"),
            })

        common_prefixes = [
            cp["Prefix"] for cp in list_response.get("CommonPrefixes", [])
        ]

        return cls(
            bucket=bucket,
            prefix=prefix,
            objects=objects,
            common_prefixes=common_prefixes,
            is_truncated=list_response.get("IsTruncated", False),
            next_continuation_token=list_response.get("NextContinuationToken"),
            max_keys=list_response.get("MaxKeys"),
        )
