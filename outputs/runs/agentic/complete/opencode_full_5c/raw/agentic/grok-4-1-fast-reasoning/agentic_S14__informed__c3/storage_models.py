from dataclasses import dataclass
from typing import Optional


@dataclass
class ObjectMetadata:
    size: int
    etag: str
    last_modified: str
    content_type: Optional[str] = None
