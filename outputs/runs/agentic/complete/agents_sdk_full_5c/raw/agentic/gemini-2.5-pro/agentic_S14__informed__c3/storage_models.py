from dataclasses import dataclass
from datetime import datetime

@dataclass
class ObjectMetadata:
    """
    A normalized data model for object metadata retrieved from storage.
    """
    name: str
    bucket: str
    size: int | None
    content_type: str | None
    updated_at: datetime | None
    etag: str | None
