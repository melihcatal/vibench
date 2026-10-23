# storage_models.py
from typing import TypedDict, Optional

# Define request/response models for object storage operations


class UploadPayload(TypedDict):
    data: bytes
    mime_type: Optional[str]


class DownloadResponse(TypedDict):
    content: bytes
    etag: str


class MetadataResponse(TypedDict):
    name: str
    size: int
    content_type: str
    created: str
    updated: str


# Normalization utilities
def normalize_object_name(name: str) -> str:
    """Normalize slashes and whitespace for provider-specific paths."""
    return name.strip().replace("\\", "/")
