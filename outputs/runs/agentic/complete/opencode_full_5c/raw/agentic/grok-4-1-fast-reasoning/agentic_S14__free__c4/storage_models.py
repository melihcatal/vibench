from typing import TypedDict, Optional, Dict


class ObjectMetadata(TypedDict):
    content_length: int
    content_type: Optional[str]
    last_modified: Optional[str]
    etag: str


def normalize_object_metadata(response: Dict) -> ObjectMetadata:
    return {
        "content_length": response["ContentLength"],
        "content_type": response.get("ContentType"),
        "last_modified": response["LastModified"].isoformat()
        if response.get("LastModified")
        else None,
        "etag": response["ETag"].strip('"'),
    }
