from typing import TypedDict, Dict, Any, List, Optional
from datetime import datetime

class UploadRequest(TypedDict):
    bucket: str
    key: str
    data: bytes
    content_type: Optional[str]

class ObjectMetadata(TypedDict):
    ETag: str
    ContentLength: int
    LastModified: datetime
    ContentType: Optional[str]
    Metadata: Dict[str, str]

class ListPrefixRequest(TypedDict):
    bucket: str
    prefix: str

class ListPrefixResponse(TypedDict):
    keys: List[str]
    common_prefixes: List[str]