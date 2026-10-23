from typing import TypedDict, List, Optional
from datetime import datetime

class ObjectInfo(TypedDict):
    key: str
    size: int
    last_modified: Optional[datetime]
    etag: Optional[str]