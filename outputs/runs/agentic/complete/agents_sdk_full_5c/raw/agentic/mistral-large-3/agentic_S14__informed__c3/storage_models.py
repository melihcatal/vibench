from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PrefixObject:
    object_key: str
    size: int
    last_modified: datetime

@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: List[PrefixObject]

@dataclass
class ObjectMetadataResponse:
    bucket: str
    object_key: str
    size: int
    content_type: Optional[str]
    etag: Optional[str]
    last_modified: Optional[datetime]
    metadata: Dict[str, str]