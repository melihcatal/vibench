from typing import TypedDict, Optional

class ObjectMetadata(TypedDict):
    name: str
    size: int
    content_type: Optional[str]
    created: Optional[str]
    updated: Optional[str]
    metadata: Optional[dict]

class ListResponse(TypedDict):
    objects: list[ObjectMetadata]
    prefixes: Optional[list[str]]
