from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class StorageObject:
    """Represents a single object stored in managed object storage."""
    key: str
    size: int
    last_modified: datetime
    e_tag: str

@dataclass
class ListObjectsRequest:
    """Request parameters for listing objects in a bucket."""
    bucket_name: str
    prefix: Optional[str] = None
    delimiter: Optional[str] = None
    max_keys: Optional[int] = None
    start_after: Optional[str] = None
    continuation_token: Optional[str] = None

@dataclass
class ListObjectsResponse:
    """Response containing a list of stored objects and common prefixes."""
    objects: List[StorageObject]
    common_prefixes: List[str]
    is_truncated: bool
    next_continuation_token: Optional[str] = None

@dataclass
class UploadObjectRequest:
    """Request parameters for uploading an object to a bucket."""
    bucket_name: str
    object_name: str
    content_type: str
    data: bytes
    metadata: Optional[Dict[str, str]] = None

@dataclass
class UploadObjectResponse:
    """Response after successfully uploading an object."""
    object_name: str
    e_tag: str
    version_id: Optional[str] = None

@dataclass
class GetObjectMetadataRequest:
    """Request parameters for getting an object's metadata."""
    bucket_name: str
    object_name: str

@dataclass
class GetObjectMetadataResponse:
    """Response containing an object's metadata."""
    object_name: str
    size: int
    last_modified: datetime
    e_tag: str
    content_type: str
    metadata: Dict[str, str]