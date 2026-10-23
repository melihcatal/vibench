from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union


@dataclass
class BucketConfig:
    bucket_name: str
    project_id: Optional[str] = None


@dataclass
class ObjectUploadRequest:
    bucket_name: str
    object_name: str
    data: Union[bytes, str]
    content_type: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_results: Optional[int] = None


@dataclass
class ObjectMetadata:
    name: str
    bucket: str
    size: int
    content_type: Optional[str] = None
    time_created: Optional[str] = None
    updated: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
