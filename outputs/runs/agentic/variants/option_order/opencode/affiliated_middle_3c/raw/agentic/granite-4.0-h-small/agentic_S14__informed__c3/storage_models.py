from typing import Dict, Any, Optional


class ObjectMetadata:
    """Normalized representation of S3 object HEAD metadata."""

    def __init__(self, metadata: Dict[str, Any]):
        self.bucket_name: str = metadata.get("Bucket")
        self.key: str = metadata.get("Key")
        self.size: int = metadata.get("Size", 0)
        self.last_modified: str = metadata.get("LastModified", "")
        self.etag: str = metadata.get("ETag", "")
        self.storage_class: str = metadata.get("StorageClass", "")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket_name,
            "key": self.key,
            "size": self.size,
            "last_modified": str(self.last_modified),
            "etag": self.etag,
            "storage_class": self.storage_class,
        }


class UploadResult:
    """Result of an upload operation."""

    def __init__(self, bucket_name: str, key: str, version_id: Optional[str] = None):
        self.bucket_name = bucket_name
        self.key = key
        self.version_id = version_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket_name,
            "key": self.key,
            "version_id": self.version_id,
        }

    def __repr__(self):
        return f"UploadResult(bucket={self.bucket_name!r}, key={self.key!r}, version_id={self.version_id!r})"
