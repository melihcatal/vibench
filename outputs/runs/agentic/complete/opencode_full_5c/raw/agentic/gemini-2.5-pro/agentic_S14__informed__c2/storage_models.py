from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class StoredObject:
    key: str
    size: int
    last_modified: str


@dataclass
class ObjectMetadata:
    metadata: Dict[str, Any]
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    e_tag: Optional[str] = None
