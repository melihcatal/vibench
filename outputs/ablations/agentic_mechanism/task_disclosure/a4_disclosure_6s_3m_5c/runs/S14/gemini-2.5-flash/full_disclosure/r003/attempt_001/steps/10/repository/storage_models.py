import dataclasses
from typing import Dict, List, Optional, Union

@dataclasses.dataclass
class StorageObject:
    bucket_name: str
    object_name: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    e_tag: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    data: Union[bytes, str]
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class ListObjectsRequest:
    bucket_name: str
    prefix: Optional[str] = None
    delimiter: Optional[str] = None
    max_keys: Optional[int] = None
    start_after: Optional[str] = None

@dataclasses.dataclass
class ListObjectsResponse:
    bucket_name: str
    objects: List[StorageObject]
    common_prefixes: List[str]
    is_truncated: bool
    next_continuation_token: Optional[str] = None

@dataclasses.dataclass
class ObjectMetadata:
    bucket_name: str
    object_name: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    e_tag: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

class StorageError(Exception):
    pass
