from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class StoredObject:
    """Represents a basic reference to an object in storage."""

    bucket_name: str
    object_key: str


@dataclass
class ObjectMetadata:
    """Represents metadata for a stored object."""

    object_key: str
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    custom_metadata: Optional[Dict[str, str]] = None
