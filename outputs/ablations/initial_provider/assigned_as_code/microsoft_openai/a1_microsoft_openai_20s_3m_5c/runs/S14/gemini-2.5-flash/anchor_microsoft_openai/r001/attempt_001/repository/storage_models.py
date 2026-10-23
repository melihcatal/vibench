from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class UploadObjectRequest:
    object_name: str
    data: bytes
    content_type: Optional[str] = None

@dataclass
class UploadObjectResponse:
    object_name: str

@dataclass
class PresignedDownloadRequest:
    object_name: str
    expiry_minutes: int = 60

@dataclass
class PresignedDownloadResponse:
    object_name: str
    url: str

@dataclass
class ObjectMetadataRequest:
    object_name: str

@dataclass
class ObjectMetadataResponse:
    object_name: str
    size: int
    last_modified: str
    content_type: str
    metadata: Dict[str, str]

@dataclass
class ListPrefixRequest:
    prefix: str = ""
    container_name: Optional[str] = None

@dataclass
class ListedObject:
    name: str
    size: int
    last_modified: str
    content_type: Optional[str] = None

@dataclass
class ListPrefixResponse:
    objects: List[ListedObject]

