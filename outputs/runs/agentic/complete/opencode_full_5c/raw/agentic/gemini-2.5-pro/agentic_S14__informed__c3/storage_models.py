from dataclasses import dataclass
from typing import Optional, Dict, List, Any


@dataclass
class StorageObject:
    bucket: str
    key: str
    content: Optional[bytes] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class PresignedUrl:
    url: str


@dataclass
class ObjectMetadata:
    key: str
    metadata: Dict[str, Any]


@dataclass
class ObjectList:
    keys: List[str]
