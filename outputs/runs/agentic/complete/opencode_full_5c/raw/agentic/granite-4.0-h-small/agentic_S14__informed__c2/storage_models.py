from dataclasses import dataclass
from typing import Any, Dict, Optional


class B2FileMetadata:
    """Response model for Backblaze B2 file metadata."""

    file_id: str
    file_name: str
    content_length: int
    content_type: str
    upload_timestamp: int


class S3ObjectMetadata:
    """Response model for Amazon S3 HeadObject response."""

    bucket: str
    key: str
    etag: str
    size: int
    last_modified: str
    content_type: str


class GenericObjectMetadata:
    """Normalized metadata common to all providers."""

    bucket: str
    key: str
    size: int
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    content_type: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


def normalize_metadata(provider: str, raw: Any) -> GenericObjectMetadata:
    """Convert provider-specific metadata to a normalized GenericObjectMetadata."""
    if provider == "backblaze_b2":
        return GenericObjectMetadata(
            bucket="<bucket-id>",
            key=raw.file_name,
            size=raw.content_length,
            etag=raw.file_id,
            last_modified=str(raw.upload_timestamp),
            content_type=raw.content_type,
            extra={"file_id": raw.file_id},
        )
    elif provider == "amazon_s3":
        return GenericObjectMetadata(
            bucket=raw.bucket,
            key=raw.key,
            size=raw.size,
            etag=raw.etag,
            last_modified=raw.last_modified,
            content_type=raw.content_type,
            extra=raw.__dict__,
        )
    else:
        # default no-op conversion
        return GenericObjectMetadata(
            bucket="unknown",
            key="unknown",
            size=0,
            extra={"raw": raw},
        )
