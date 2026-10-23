from typing import TypedDict, List

class ObjectInfo(TypedDict):
    name: str
    size: int
    content_type: str
    updated: str
    metadata: dict

class ListResponse(TypedDict):
    objects: List[ObjectInfo]
