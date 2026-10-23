"""
Local data models and normalization helpers for Managed Object Storage operations.

Provides typed request/response dataclasses, S3 metadata normalization,
and conversion utilities for object storage operations.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class UploadRequest:
    """Normalized upload request for object storage."""
    bucket: str
    key: str
    content: Optional[bytes] = None
    file_path: Optional[str] = None
    content_type: str = "application/octet-stream"
    metadata: dict[str, str] = field(default_factory=dict)
    storage_class: str = "STANDARD"
    acl: Optional[str] = None


@dataclass
class UploadResponse:
    """Normalized response after uploading an object to S3."""
    bucket: str
    key: str
    etag: str = ""
    version_id: Optional[str] = None
    request_id: str = ""
    s3_uri: str = ""
    content_length: int = 0


@dataclass
class PresignedUrlRequest:
    """Normalized request for generating a presigned download URL."""
    bucket: str
    key: str
    method: str = "GET"
    expires_in_seconds: int = 3600
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    """Holds a presigned URL and metadata."""
    url: str = ""
    bucket: str = ""
    key: str = ""
    expires_at: Optional[datetime] = None
    method: str = "GET"


@dataclass
class ObjectMetadataRequest:
    """Normalized request for reading object metadata (HEAD object)."""
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class ObjectMetadataResponse:
    """Normalized metadata response for an S3 object."""
    bucket: str = ""
    key: str = ""
    content_type: str = ""
    content_length: int = 0
    etag: str = ""
    last_modified: Optional[datetime] = None
    storage_class: str = ""
    version_id: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
    content_encoding: Optional[str] = None
    cache_control: Optional[str] = None
    content_language: Optional[str] = None


@dataclass
class ListPrefixRequest:
    """Normalized request for listing objects under a prefix."""
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000
    start_after: str = ""


@dataclass
class ObjectSummary:
    """Summarized info for a single stored object."""
    key: str = ""
    size: int = 0
    etag: str = ""
    last_modified: Optional[datetime] = None
    storage_class: str = ""


@dataclass
class ListPrefixResponse:
    """Normalized response for a prefix listing operation."""
    bucket: str = ""
    prefix: str = ""
    objects: list[ObjectSummary] = field(default_factory=list)
    common_prefixes: list[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None


def normalize_s3_metadata(raw_headers: dict[str, Any]) -> dict[str, str]:
    """
    Extract and normalize user-defined metadata from S3 HEAD response headers.

    S3 prefixes user metadata keys with 'x-amz-meta-' in HTTP responses.
    This function strips that prefix and lowercases the keys.
    """
    prefix = "x-amz-meta-"
    normalized = {}
    for key, value in raw_headers.items():
        lower_key = key.lower()
        if lower_key.startswith(prefix):
            normalized[lower_key[len(prefix):]] = str(value)
    return normalized


def parse_last_modified(raw_ts: Any) -> Optional[datetime]:
    """Parse an S3 LastModified timestamp into a datetime."""
    if raw_ts is None:
        return None
    if isinstance(raw_ts, datetime):
        return raw_ts
    # Try common formats
    from email.utils import parsedate_to_datetime
    if isinstance(raw_ts, str):
        return parsedate_to_datetime(raw_ts)
    return None


def build_content_disposition(filename: str) -> str:
    """Build a Content-Disposition header value for download."""
    safe_name = os.path.basename(filename).replace('"', "")
    return f'attachment; filename="{safe_name}"'


def ocr_extraction_result_to_text(extraction: dict[str, Any]) -> str:
    """
    Normalize an OCR extraction result into plain text.

    Handles common provider output shapes:
    - Textract-style Blocks
    - Generic pages/lines/words structure
    - Raw text field
    """
    if isinstance(extraction, str):
        return extraction

    if "Blocks" in extraction:
        # Amazon Textract style
        text_parts = []
        for block in extraction["Blocks"]:
            if block.get("BlockType") == "LINE":
                text_parts.append(block.get("Text", ""))
        return "\n".join(text_parts)

    if "pages" in extraction:
        # Generic pages/lines structure
        text_parts = []
        for page in extraction["pages"]:
            for line in page.get("lines", []):
                text_parts.append(line.get("text", line.get("content", "")))
        return "\n".join(text_parts)

    if "text" in extraction:
        return str(extraction["text"])

    if "content" in extraction:
        return str(extraction["content"])

    return str(extraction)
