from typing import TypedDict, Dict, Any, List, Optional


class ObjectMetadata(TypedDict):
    content_length: int
    content_type: Optional[str]
    last_modified: str
    etag: str
    metadata: Dict[str, str]


class ObjectSummary(TypedDict):
    key: str
    size: int
    last_modified: str
    etag: str


def parse_object_metadata(resp: Dict[str, Any]) -> ObjectMetadata:
    return {
        "content_length": resp["ContentLength"],
        "content_type": resp.get("ContentType"),
        "last_modified": resp["LastModified"].isoformat(),
        "etag": resp["ETag"].strip('"'),
        "metadata": dict(resp.get("Metadata", {})),
    }


def parse_object_summary(content: Dict[str, Any]) -> ObjectSummary:
    return {
        "key": content["Key"],
        "size": content["Size"],
        "last_modified": content["LastModified"].isoformat(),
        "etag": content["ETag"].strip('"'),
    }
