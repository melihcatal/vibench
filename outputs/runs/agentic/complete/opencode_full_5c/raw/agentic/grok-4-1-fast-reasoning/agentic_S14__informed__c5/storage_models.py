from typing import TypedDict, Dict, Any, List


class ObjectMetadata(TypedDict):
    content_length: int
    content_type: str
    etag: str
    last_modified: str
    metadata: Dict[str, str]


def normalize_object_metadata(raw: Dict[str, Any]) -> ObjectMetadata:
    return {
        "content_length": raw["ContentLength"],
        "content_type": raw.get("ContentType", ""),
        "etag": raw["ETag"],
        "last_modified": str(raw["LastModified"]),
        "metadata": dict(raw.get("Metadata", {})),
    }
