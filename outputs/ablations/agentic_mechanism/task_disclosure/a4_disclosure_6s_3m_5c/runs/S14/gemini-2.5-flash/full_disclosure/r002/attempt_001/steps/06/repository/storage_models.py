import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class StorageObject:
    bucket_name: str
    object_key: str
    size: Optional[int] = None
    last_modified: Optional[datetime.datetime] = None
    content_type: Optional[str] = None
    e_tag: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class UploadRequest:
    bucket_name: str
    object_key: str
    data: bytes
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class UploadResponse:
    bucket_name: str
    object_key: str
    e_tag: Optional[str] = None
    version_id: Optional[str] = None
    upload_success: bool = False
    message: Optional[str] = None

@dataclass
class ListObjectsRequest:
    bucket_name: str
    prefix: Optional[str] = None
    max_keys: Optional[int] = None
    delimiter: Optional[str] = None
    start_after: Optional[str] = None

@dataclass
class ListObjectsResponse:
    bucket_name: str
    prefix: Optional[str] = None
    objects: List[StorageObject] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None

def normalize_object_key(key: str) -> str:
    """Normalizes an object key by stripping leading/trailing slashes."""
    return key.strip('/')
