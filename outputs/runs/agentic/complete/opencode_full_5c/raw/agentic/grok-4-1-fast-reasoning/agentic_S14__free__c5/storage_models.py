from typing import TypedDict, List, Optional, Dict


class ObjectMetadata(TypedDict):
    content_type: Optional[str]
    content_length: int
    last_modified: Optional[str]
    metadata: Dict[str, str]


class ObjectInfo(TypedDict):
    key: str
    size: int
    last_modified: str
    etag: str


ListObjectsResponse = List[ObjectInfo]
