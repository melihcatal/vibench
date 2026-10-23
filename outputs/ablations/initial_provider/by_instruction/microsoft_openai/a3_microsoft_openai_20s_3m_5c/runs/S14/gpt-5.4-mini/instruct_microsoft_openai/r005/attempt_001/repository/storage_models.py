from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class UploadRequest:
    container_name: str
    blob_name: str
    data: Any
    overwrite: bool = True
    content_type: Optional[str] = None


@dataclass
class StorageObjectMetadata:
    container_name: str
    blob_name: str
    etag: Optional[str]
    last_modified: Optional[str]
    content_length: Optional[int]
    content_type: Optional[str]
    metadata: Dict[str, str]


def normalize_blob_listing(items: Iterable[Any]) -> List[Dict[str, Any]]:
    result = []
    for item in items:
        result.append({
            "name": getattr(item, "name", None),
            "container": getattr(item, "container", None),
            "size": getattr(item, "size", None),
            "last_modified": getattr(item, "last_modified", None).isoformat() if getattr(item, "last_modified", None) else None,
        })
    return result
