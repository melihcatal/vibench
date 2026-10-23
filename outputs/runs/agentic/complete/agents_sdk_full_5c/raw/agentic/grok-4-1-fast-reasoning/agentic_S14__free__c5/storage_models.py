from typing import TypedDict, List, Dict, Any

class S3ObjectSummary(TypedDict):
    Key: str
    Size: int
    LastModified: Any
    ETag: str
    StorageClass: str

class ObjectHeadResponse(TypedDict):
    ContentLength: int
    ContentType: str
    ContentEncoding: str
    LastModified: Any
    ETag: str
    Metadata: Dict[str, str]

class ListObjectsResponse(TypedDict):
    Contents: List[S3ObjectSummary]
    CommonPrefixes: List[Dict[str, str]]
    IsTruncated: bool
    MaxKeys: int
