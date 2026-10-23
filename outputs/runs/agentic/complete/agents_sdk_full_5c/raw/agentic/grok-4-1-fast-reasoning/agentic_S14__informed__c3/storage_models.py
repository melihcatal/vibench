from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class ObjectMetadata:
    key: str
    e_tag: str
    size: int
    last_modified: datetime
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclass
class ObjectListResponse:
    contents: List[ObjectMetadata]
    is_truncated: bool
    next_continuation_token: Optional[str] = None