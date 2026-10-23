import dataclasses
from datetime import datetime
from typing import Dict, Any, Optional

@dataclasses.dataclass
class StoredObject:
    bucket_name: str
    object_name: str
    size: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class UploadFileRequest:
    bucket_name: str
    object_name: str
    file_content: bytes
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class StorageResponse:
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

def normalize_object_name(name: str) -> str:
    """Normalizes an object name for storage, e.g., removing leading/trailing slashes."""
    return name.strip('/')

def parse_s3_metadata(raw_metadata: Dict[str, str]) -> Dict[str, Any]:
    """Parses raw metadata from S3-like services, converting all keys to lowercase."""
    return {k.lower(): v for k, v in raw_metadata.items()}
