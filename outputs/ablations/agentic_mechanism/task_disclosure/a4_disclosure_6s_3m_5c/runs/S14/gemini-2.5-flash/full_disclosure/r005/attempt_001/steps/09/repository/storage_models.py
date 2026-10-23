import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class StorageObject:
    bucket_name: str
    object_name: str
    object_path: Optional[str] = None

@dataclasses.dataclass
class ObjectMetadata:
    storage_object: StorageObject
    metadata: Dict[str, Any]

@dataclasses.dataclass
class UploadObjectRequest:
    storage_object: StorageObject
    content: bytes
    content_type: str

@dataclasses.dataclass
class DownloadObjectResponse:
    storage_object: StorageObject
    content: bytes
    content_type: str
