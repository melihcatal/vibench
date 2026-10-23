from typing import Dict, Optional, Union
from dataclasses import dataclass


@dataclass
class UploadRequest:
    """Request model for uploading an object."""

    bucket_name: str
    object_key: str
    body: Union[bytes, object]
    content_type: str = "application/octet-stream"
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    """Response model for object upload."""

    etag: str
    version_id: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    """Request model for generating a presigned download URL."""

    bucket_name: str
    object_key: str
    expiration: int = 3600


@dataclass
class PresignedDownloadResponse:
    """Response model for presigned download URL."""

    url: str


@dataclass
class ObjectMetadataRequest:
    """Request model for retrieving object metadata."""

    bucket_name: str
    object_key: str


@dataclass
class ObjectMetadataResponse:
    """Response model for object metadata."""

    content_type: Optional[str] = None
    etag: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListPrefixRequest:
    """Request model for listing objects under a prefix."""

    bucket_name: str
    prefix: str = ""
    max_keys: int = 1000


@dataclass
class ListPrefixResponse:
    """Response model for listing objects under a prefix."""

    objects: list[dict]


def normalize_metadata(metadata: Dict[str, str]) -> Dict[str, str]:
    """
    Normalizes metadata keys to lowercase for consistency.

    Args:
        metadata: Dictionary of metadata key-value pairs.

    Returns:
        Dictionary with normalized keys.
    """
    return {k.lower(): v for k, v in metadata.items()}
