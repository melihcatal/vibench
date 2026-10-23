import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None

@dataclasses.dataclass
class UploadObjectResponse:
    e_tag: str
    version_id: Optional[str] = None

@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expires_in: int = 3600  # Seconds

@dataclasses.dataclass
class PresignedDownloadResponse:
    url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    metadata: Dict[str, Any]

@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000

@dataclasses.dataclass
class ListPrefixResponse:
    object_keys: list[str]
    common_prefixes: list[str]
