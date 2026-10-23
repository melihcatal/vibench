from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): "" if v is None else str(v) for k, v in metadata.items()}


def normalize_list_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items:
        normalized.append({
            "name": str(item.get("name", "")),
            "size": int(item.get("size", 0) or 0),
            "last_modified": item.get("last_modified"),
            "etag": item.get("etag"),
        })
    return normalized


@dataclass
class UploadResult:
    object_name: str
    etag: Optional[str]
    url: Optional[str]


@dataclass
class PresignedUrlResult:
    object_name: str
    url: str
    expires_in: int


@dataclass
class MetadataResult:
    object_name: str
    metadata: Dict[str, str]
    content_type: Optional[str]
    content_length: Optional[int]
