from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class UploadObjectRequest:
    container_name: str
    blob_name: str
    data: bytes
    content_settings: Optional[Dict[str, str]] = None

@dataclass
class UploadObjectResponse:
    success: bool
    e_tag: Optional[str] = None
    last_modified: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    container_name: str
    blob_name: str
    expiry_minutes: int

@dataclass
class PresignedDownloadResponse:
    success: bool
    url: Optional[str] = None

@dataclass
class ObjectMetadataRequest:
    container_name: str
    blob_name: str

@dataclass
class ObjectMetadata:
    name: str
    size: int
    last_modified: str
    e_tag: str
    content_settings: Dict[str, str]
    metadata: Dict[str, str]

@dataclass
class ListPrefixRequest:
    container_name: str
    prefix: str

@dataclass
class ListPrefixResponse:
    success: bool
    blob_names: List[str]
