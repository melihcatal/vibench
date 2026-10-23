"""
Local request, response, and normalization helpers for Managed Object Storage (AWS S3).

Defines dataclasses for upload, download, metadata, and listing operations,
along with utility functions for normalizing S3 responses into consistent shapes.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import IO, Any, Dict, List, Optional


@dataclass
class UploadRequest:
    """Represents parameters for uploading an object to S3."""
    bucket: str
    key: str
    body: Optional[bytes] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    storage_class: Optional[str] = None

    def resolve_body(self) -> bytes:
        """Resolve the upload body from either bytes or file path."""
        if self.body is not None:
            return self.body
        if self.file_path:
            with open(self.file_path, "rb") as fh:
                return fh.read()
        raise ValueError("Either body or file_path must be provided")


@dataclass
class UploadResponse:
    """Normalized response from an S3 upload operation."""
    bucket: str
    key: str
    etag: str = ""
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    content_length: int = 0
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PresignedURLRequest:
    """Parameters for generating a presigned download URL."""
    bucket: str
    key: str
    expires_in_seconds: int = 3600
    http_method: str = "GET"
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedURLResponse:
    """Result of generating a presigned URL."""
    url: str
    bucket: str
    key: str
    expires_in_seconds: int
    method: str


@dataclass
class ObjectMetadataRequest:
    """Parameters for reading object metadata (HeadObject)."""
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class ObjectMetadataResponse:
    """Normalized S3 object metadata."""
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    last_modified: Optional[datetime] = None
    etag: str = ""
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    delete_marker: bool = False


@dataclass
class ListPrefixRequest:
    """Parameters for listing objects under a prefix."""
    bucket: str
    prefix: str
    delimiter: Optional[str] = None
    max_keys: int = 1000
    start_after: Optional[str] = None


@dataclass
class ListedObject:
    """A single object entry from an S3 listing."""
    key: str
    size: int = 0
    last_modified: Optional[datetime] = None
    etag: str = ""
    storage_class: str = "STANDARD"
    is_common_prefix: bool = False


@dataclass
class ListPrefixResponse:
    """Normalized listing result."""
    bucket: str
    prefix: str
    objects: List[ListedObject] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0


def normalize_upload_response(raw: Dict[str, Any], bucket: str, key: str) -> UploadResponse:
    """Normalize a raw S3 put_object response."""
    return UploadResponse(
        bucket=bucket,
        key=key,
        etag=raw.get("ETag", "").strip('"'),
        version_id=raw.get("VersionId"),
        storage_class=raw.get("StorageClass"),
        content_length=raw.get("ContentLength", 0),
        raw_response=raw,
    )


def normalize_head_response(raw: Dict[str, Any], bucket: str, key: str) -> ObjectMetadataResponse:
    """Normalize a raw S3 head_object response."""
    metadata = {}
    for mk, mv in raw.get("Metadata", {}).items():
        metadata[mk.lower()] = mv

    return ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        content_type=raw.get("ContentType"),
        content_length=raw.get("ContentLength", 0),
        last_modified=raw.get("LastModified"),
        etag=raw.get("ETag", "").strip('"'),
        version_id=raw.get("VersionId"),
        storage_class=raw.get("StorageClass", "STANDARD"),
        metadata=metadata,
        delete_marker=raw.get("DeleteMarker", False),
    )


def normalize_listed_object(raw: Dict[str, Any]) -> ListedObject:
    """Normalize a single S3 object listing entry."""
    return ListedObject(
        key=raw.get("Key", ""),
        size=raw.get("Size", 0),
        last_modified=raw.get("LastModified"),
        etag=raw.get("ETag", "").strip('"'),
        storage_class=raw.get("StorageClass", "STANDARD"),
    )


def normalize_list_response(raw: Dict[str, Any], bucket: str, prefix: str) -> ListPrefixResponse:
    """Normalize a raw S3 list_objects_v2 response."""
    objects = [normalize_listed_object(obj) for obj in raw.get("Contents", [])]
    common_prefixes = [
        cp.get("Prefix", "")
        for cp in raw.get("CommonPrefixes", [])
    ]
    return ListPrefixResponse(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        common_prefixes=common_prefixes,
        is_truncated=raw.get("IsTruncated", False),
        next_continuation_token=raw.get("NextContinuationToken"),
        key_count=raw.get("KeyCount", len(objects)),
    )
