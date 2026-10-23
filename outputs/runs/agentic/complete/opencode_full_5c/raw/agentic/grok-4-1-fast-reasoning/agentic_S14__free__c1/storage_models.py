from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ObjectMetadata:
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class ListedObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None


def normalize_metadata(raw: Dict[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        content_length=raw.get("ContentLength"),
        content_type=raw.get("ContentType"),
        last_modified=raw["LastModified"].isoformat()
        if "LastModified" in raw
        else None,
        etag=raw.get("ETag"),
    )


def normalize_list(raw_objects: List[Dict[str, Any]]) -> List[ListedObject]:
    return [
        ListedObject(
            key=obj["Key"],
            size=obj.get("Size"),
            last_modified=obj["LastModified"].isoformat()
            if "LastModified" in obj
            else None,
        )
        for obj in raw_objects
    ]
