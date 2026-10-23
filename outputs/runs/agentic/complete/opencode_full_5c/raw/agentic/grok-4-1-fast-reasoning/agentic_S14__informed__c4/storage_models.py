from typing import TypedDict, List, Optional, Dict, Any


class UploadResponse(TypedDict):
    etag: str
    version_id: Optional[str]


class ObjectMetadata(TypedDict):
    key: str
    size: int
    etag: str
    last_modified: str
    content_type: Optional[str]
    metadata: Optional[Dict[str, str]]


class ListObjectsResult(TypedDict):
    objects: List[ObjectMetadata]
    is_truncated: bool
    common_prefixes: List[str]
