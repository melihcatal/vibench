from typing import Dict, Any, Optional

class StorageObject:
    """
    Represents an object stored in object storage.
    """
    def __init__(self, bucket_name: str, key: str, size: Optional[int] = None, last_modified: Optional[str] = None):
        self.bucket_name = bucket_name
        self.key = key
        self.size = size
        self.last_modified = last_modified

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket_name": self.bucket_name,
            "key": self.key,
            "size": self.size,
            "last_modified": self.last_modified
        }

class ObjectMetadata:
    """
    Represents metadata for an object in object storage.
    """
    def __init__(self, etag: str, content_type: str, content_length: int, last_modified: str, custom_metadata: Optional[Dict[str, str]] = None):
        self.etag = etag
        self.content_type = content_type
        self.content_length = content_length
        self.last_modified = last_modified
        self.custom_metadata = custom_metadata if custom_metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ETag": self.etag,
            "ContentType": self.content_type,
            "ContentLength": self.content_length,
            "LastModified": self.last_modified,
            "CustomMetadata": self.custom_metadata
        }
