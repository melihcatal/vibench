from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class StorageObject:
    """
    A simple data class to hold object metadata.
    """
    name: str
    bucket: str
    size: Optional[int]
    content_type: Optional[str]
    updated: Optional[datetime]
