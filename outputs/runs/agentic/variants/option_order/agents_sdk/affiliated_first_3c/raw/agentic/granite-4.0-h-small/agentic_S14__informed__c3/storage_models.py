from typing import TypedDict, List

class ObjectMetadata(TypedDict):
    Key: str
    Size: int
    StorageClass: str
    LastModified: str
    ETag: str
    Metadata: dict

class ListObjectsResponse(TypedDict):
    Contents: List[ObjectMetadata]
    CommonPrefixes: List[str] | None
