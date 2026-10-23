from typing import Dict, Optional, TypedDict


class UploadRequest(TypedDict):
    """Request model for uploading an object."""

    bucket_name: str
    object_key: str
    content_type: str
    metadata: Optional[Dict[str, str]]


class UploadResponse(TypedDict):
    """Response model for upload operations."""

    object_key: str
    etag: str


class PresignedDownloadRequest(TypedDict):
    """Request model for generating a presigned download URL."""

    bucket_name: str
    object_key: str
    expiration: int


class PresignedDownloadResponse(TypedDict):
    """Response model for presigned download URL operations."""

    presigned_url: str


class ObjectMetadataResponse(TypedDict):
    """Response model for object metadata operations."""

    content_type: Optional[str]
    content_length: Optional[int]
    etag: Optional[str]
    last_modified: Optional[str]
    metadata: Dict[str, str]


class ListObjectsRequest(TypedDict):
    """Request model for listing objects by prefix."""

    bucket_name: str
    prefix: str
    max_keys: int


class ListObjectsResponse(TypedDict):
    """Response model for listing objects operations."""

    objects: list[dict]


def normalize_metadata(metadata: Dict[str, Optional[str]]) -> ObjectMetadataResponse:
    """
    Normalizes raw S3 metadata into a standardized response format.

    Args:
        metadata: Raw metadata dictionary from S3.

    Returns:
        ObjectMetadataResponse: Normalized metadata response.
    """
    return {
        "content_type": metadata.get("ContentType"),
        "content_length": metadata.get("ContentLength"),
        "etag": metadata.get("ETag"),
        "last_modified": metadata.get("LastModified"),
        "metadata": metadata.get("Metadata", {}),
    }
