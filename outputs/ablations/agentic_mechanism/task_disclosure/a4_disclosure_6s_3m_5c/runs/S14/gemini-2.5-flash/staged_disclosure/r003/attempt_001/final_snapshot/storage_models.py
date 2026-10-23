
import dataclasses
from typing import Any, Dict, Optional

@dataclasses.dataclass
class StorageRequest:
    bucket_name: str
    object_name: str
    data: Optional[bytes] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class StorageResponse:
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

def normalize_object_name(object_name: str) -> str:
    """Normalizes an object name for storage, e.g., removes leading/trailing slashes."""
    if not object_name:
        return ""
    # Remove leading/trailing slashes and replace multiple slashes with a single one
    normalized = "/".join(part for part in object_name.strip("/").split("/") if part)
    return normalized
