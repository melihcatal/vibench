from typing import TypedDict, Optional

class ObjectMetadata(TypedDict):
    key: str
    size: int
    last_modified: str  # ISO8601 string
    etag: str
    storage_class: str

class ListObject(TypedDict):
    Key: str
    Size: int
    LastModified: str
    ETag: str
    StorageClass: str

class StorageError(TypedDict):
    code: str
    message: str

def normalize_metadata(raw: Dict[str, Any]) -> ObjectMetadata:
    """Convert raw boto3 head_object output to a simplified TypedDict."""
    return {
        "key": raw['Key'],
        "size": raw.get('ContentLength', 0),
        "last_modified": raw['LastModified'].isoformat(),
        "etag": raw['ETag'],
        "storage_class": raw['StorageClass'],
    }
