"""
Local request, response, and normalization helpers for Managed Object Storage.

Defines data classes for upload, download, metadata, and listing operations
used across S3 managed object storage integration files.
"""

import io
import mimetypes
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, BinaryIO, Dict, List, Optional, Union


# Standard MIME types for common file extensions
DEFAULT_MIME_TYPES = {
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".json": "application/json",
    ".csv": "text/csv",
    ".html": "text/html",
    ".xml": "application/xml",
    ".zip": "application/zip",
    ".mp4": "video/mp4",
    ".mp3": "audio/mpeg",
    ".docx": (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ),
    ".xlsx": (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ),
}


@dataclass
class StorageObjectRequest:
    """Request model for uploading or interacting with a storage object."""

    bucket: str
    key: str
    data: Optional[Union[bytes, BinaryIO, io.BytesIO]] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    storage_class: Optional[str] = None
    content_encoding: Optional[str] = None
    cache_control: Optional[str] = None
    server_side_encryption: Optional[str] = None
    acl: Optional[str] = None
    tags: Optional[Dict[str, str]] = None

    def resolve_content_type(self) -> str:
        """Resolve content type from explicit value or file extension."""
        if self.content_type:
            return self.content_type
        if self.file_path:
            guessed, _ = mimetypes.guess_type(self.file_path)
            if guessed:
                return guessed
            ext = "." + self.file_path.rsplit(".", 1)[-1].lower() if "." in self.file_path else ""
            return DEFAULT_MIME_TYPES.get(ext, "application/octet-stream")
        if self.key:
            guessed, _ = mimetypes.guess_type(self.key)
            if guessed:
                return guessed
            ext = "." + self.key.rsplit(".", 1)[-1].lower() if "." in self.key else ""
            return DEFAULT_MIME_TYPES.get(ext, "application/octet-stream")
        return "application/octet-stream"

    def get_data_stream(self) -> Union[bytes, BinaryIO]:
        """Get the data to upload, loading from file if needed."""
        if self.data is not None:
            return self.data
        if self.file_path:
            return open(self.file_path, "rb")
        raise ValueError("No data or file_path provided in request")


@dataclass
class StorageUploadResponse:
    """Response model for an upload operation."""

    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    content_type: Optional[str] = None
    content_length: int = 0
    server_side_encryption: Optional[str] = None
    expiration: Optional[str] = None
    request_id: Optional[str] = None
    s3_uri: Optional[str] = None
    upload_timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StorageObjectMetadata:
    """Response model for object metadata / HEAD operation."""

    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None
    content_encoding: Optional[str] = None
    cache_control: Optional[str] = None
    expires: Optional[datetime] = None
    website_redirect_location: Optional[str] = None
    s3_uri: Optional[str] = None
    exists: bool = True


@dataclass
class StorageObjectListing:
    """Response model for a prefix-based listing operation."""

    bucket: str
    prefix: str
    objects: List["ObjectSummary"] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    max_keys: int = 1000
    key_count: int = 0
    delimiter: Optional[str] = None


@dataclass
class ObjectSummary:
    """Summary information for a single listed object."""

    key: str
    size: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    owner_id: Optional[str] = None
    s3_uri: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    """Response model for a presigned URL operation."""

    url: str
    bucket: str
    key: str
    expires_in: int = 3600
    http_method: str = "GET"
    generated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


def normalize_metadata(
    raw_metadata: Optional[Dict[str, Any]]
) -> Dict[str, str]:
    """Normalize metadata dict to string-string pairs for S3 user metadata."""
    if raw_metadata is None:
        return {}
    result = {}
    for k, v in raw_metadata.items():
        key_str = str(k).lower().replace("_", "-")
        if not key_str.startswith("x-amz-meta-"):
            key_str = f"x-amz-meta-{key_str}"
        result[key_str] = str(v)
    return result


def parse_metadata_from_s3_response(
    response: Dict[str, Any]
) -> Dict[str, str]:
    """Extract user metadata from an S3 response dict."""
    metadata = {}
    for key, value in response.items():
        if key.lower().startswith("x-amz-meta-"):
            metadata[key] = str(value)
    return metadata


def format_size_human(size_bytes: int) -> str:
    """Format byte size into human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def parse_s3_response_to_metadata(
    response: Dict[str, Any], bucket: str, key: str
) -> StorageObjectMetadata:
    """Parse an S3 HeadObject or GetObject response into StorageObjectMetadata."""
    from storage_client import format_s3_uri

    return StorageObjectMetadata(
        bucket=bucket,
        key=key,
        content_type=response.get("ContentType"),
        content_length=response.get("ContentLength", 0),
        etag=response.get("ETag", "").strip('"'),
        last_modified=response.get("LastModified"),
        storage_class=response.get("StorageClass"),
        version_id=response.get("VersionId"),
        metadata=parse_metadata_from_s3_response(response),
        server_side_encryption=response.get("ServerSideEncryption"),
        content_encoding=response.get("ContentEncoding"),
        cache_control=response.get("CacheControl"),
        expires=response.get("Expires"),
        website_redirect_location=response.get("WebsiteRedirectLocation"),
        s3_uri=format_s3_uri(bucket, key),
    )


def parse_s3_list_response(
    response: Dict[str, Any], bucket: str, prefix: str
) -> StorageObjectListing:
    """Parse an S3 list_objects_v2 response into StorageObjectListing."""
    from storage_client import format_s3_uri

    objects = []
    for item in response.get("Contents", []):
        objects.append(
            ObjectSummary(
                key=item["Key"],
                size=item.get("Size", 0),
                etag=item.get("ETag", "").strip('"'),
                last_modified=item.get("LastModified"),
                storage_class=item.get("StorageClass"),
                owner_id=item.get("Owner", {}).get("ID"),
                s3_uri=format_s3_uri(bucket, item["Key"]),
            )
        )

    common_prefixes = [
        cp["Prefix"] for cp in response.get("CommonPrefixes", [])
    ]

    return StorageObjectListing(
        bucket=bucket,
        prefix=prefix,
        objects=objects,
        common_prefixes=common_prefixes,
        is_truncated=response.get("IsTruncated", False),
        next_continuation_token=response.get("NextContinuationToken"),
        max_keys=response.get("MaxKeys", 1000),
        key_count=response.get("KeyCount", len(objects)),
        delimiter=response.get("Delimiter"),
    )
