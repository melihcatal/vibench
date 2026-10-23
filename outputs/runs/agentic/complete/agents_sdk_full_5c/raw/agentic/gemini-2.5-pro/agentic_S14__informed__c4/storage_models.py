from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ObjectMetadata:
    key: str
    size: int
    last_modified: datetime
    etag: str
    content_type: Optional[str] = None
    version_id: Optional[str] = None

@dataclass
class PresignedUrl:
    url: str
    key: str
    method: str

@dataclass
class ObjectSummary:
    key: str
    size: int
    last_modified: datetime
