from typing import TypedDict, List, Dict, Any

class ObjectMetadata(TypedDict):
    etag: str
    size: int
    content_type: str | None
    last_modified: str | None
    metadata: Dict[str, Any] | None

class ListObjectsResponse(TypedDict):
    objects: List[Dict[str, Any]]
    prefixes: List[str]
    is_truncated: bool
    next_continuation_token: str | None
