'''Local models and helpers for object storage interactions.'''
from datetime import datetime
from typing import TypedDict, Optional

class UploadResult(TypedDict):
    """Result of an upload operation."""
    container: str
    blob: str
    size: int

class PresignedDownloadInfo(TypedDict):
    """Info returned by presigned download generation."""
    url: str
    expires_at: datetime

class ObjectMetadataResult(TypedDict):
    """Metadata returned by HEAD request."""
    container: str
    blob: str
    size: int
    last_modified: datetime
    content_type: str
    etag: str
    metadata: Optional[dict]

class PrefixListResult(TypedDict):
    """Result of a prefix listing operation."""
    container: str
    prefix: str
    blobs: List[str]
