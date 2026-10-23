from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UploadObjectRequest:
    bucket: str
    key: str
    body: Any
    content_type: Optional[str] = None


@dataclass
class ObjectMetadata:
    bucket: str
    key: str
    metadata: Dict[str, Any]


def normalize_list_objects(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    contents = response.get("Contents", []) or []
    return [
        {
            "key": item.get("Key"),
            "size": item.get("Size"),
            "last_modified": item.get("LastModified").isoformat()
            if item.get("LastModified")
            else None,
        }
        for item in contents
    ]
