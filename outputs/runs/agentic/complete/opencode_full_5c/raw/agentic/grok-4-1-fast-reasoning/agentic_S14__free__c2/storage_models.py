from typing import TypedDict, Dict, Any, List, Optional


class S3ObjectMetadata(TypedDict):
    ETag: str
    Size: int
    LastModified: str
    ContentType: Optional[str]
    Metadata: Dict[str, str]


class S3ListResponse(TypedDict):
    Contents: List[Dict[str, Any]]
    CommonPrefixes: List[str]
    IsTruncated: bool
