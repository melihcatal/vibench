from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_object_name(value: str) -> str:
    return value.lstrip("/")


@dataclass
class UploadRequest:
    object_name: str
    content_type: Optional[str] = None


@dataclass
class ObjectMetadata:
    name: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    updated: Optional[str] = None
    etag: Optional[str] = None


def metadata_from_blob(blob: Any) -> ObjectMetadata:
    return ObjectMetadata(
        name=blob.name,
        size=getattr(blob, "size", None),
        content_type=getattr(blob, "content_type", None),
        updated=str(getattr(blob, "updated", None))
        if getattr(blob, "updated", None)
        else None,
        etag=getattr(blob, "etag", None),
    )


def metadata_to_dict(metadata: ObjectMetadata) -> Dict[str, Any]:
    return {
        "name": metadata.name,
        "size": metadata.size,
        "content_type": metadata.content_type,
        "updated": metadata.updated,
        "etag": metadata.etag,
    }
