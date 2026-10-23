from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ObjectReference:
    bucket: str
    key: str


def normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(metadata)
    if "ContentLength" in normalized:
        normalized["content_length"] = normalized.pop("ContentLength")
    if "ContentType" in normalized:
        normalized["content_type"] = normalized.pop("ContentType")
    if "ETag" in normalized:
        normalized["etag"] = normalized.pop("ETag")
    return normalized


def normalize_list_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "key": item.get("Key"),
        "last_modified": item.get("LastModified"),
        "etag": item.get("ETag"),
        "size": item.get("Size"),
        "storage_class": item.get("StorageClass"),
    }
