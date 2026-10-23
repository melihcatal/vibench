from typing import Dict, Optional, TypedDict
from dataclasses import dataclass


class ObjectMetadataResponse(TypedDict):
    name: str
    size: int
    content_type: str
    time_created: str
    updated: str
    metadata: Optional[Dict[str, str]]


@dataclass
class UploadRequest:
    object_name: str
    data: bytes
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_in_seconds: int