from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ObjectMetadata:
    name: str
    bucket: str
    size: int
    content_type: Optional[str]
    time_created: Any
    time_updated: Any
    custom_metadata: Optional[Dict[str, str]] = None


@dataclass
class PresignedUrlResponse:
    object_name: str
    signed_url: str
    expiration: int


@dataclass
class UploadResponse:
    bucket: str
    object_name: str
    success: bool
    size: Optional[int] = None
