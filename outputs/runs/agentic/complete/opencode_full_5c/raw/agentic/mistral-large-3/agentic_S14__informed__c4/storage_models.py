from typing import Dict, Optional, Union, IO
from dataclasses import dataclass


@dataclass
class UploadRequest:
    """Request model for uploading an object."""

    bucket_name: str
    object_key: str
    body: Union[bytes, IO]
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    """Response model for uploading an object."""

    bucket: str
    key: str
    etag: str
    version_id: Optional[str] = None


@dataclass
class ObjectMetadata:
    """Response model for object metadata."""

    content_type: Optional[str]
    content_length: Optional[int]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str]
    version_id: Optional[str] = None


@dataclass
class ListObjectsRequest:
    """Request model for listing objects."""

    bucket_name: str
    prefix: str = ""
    max_keys: int = 1000


@dataclass
class ListedObject:
    """Model for a listed object."""

    key: str
    size: int
    last_modified: str
    etag: str
    storage_class: str


@dataclass
class ListObjectsResponse:
    """Response model for listing objects."""

    objects: list[ListedObject]


def normalize_metadata(metadata: Dict[str, str]) -> Dict[str, str]:
    """Normalizes metadata keys to lowercase."""
    return {k.lower(): v for k, v in metadata.items()}
