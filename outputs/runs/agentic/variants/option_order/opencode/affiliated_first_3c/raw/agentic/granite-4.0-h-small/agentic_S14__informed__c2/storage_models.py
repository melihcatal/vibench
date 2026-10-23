class StorageModels:
    """Local normalization helpers for Managed Object Storage requests and responses.
    Provides simple data classes and utility functions to standardize payloads across integration steps.
    """

    from dataclasses import dataclass

    @dataclass
    class UploadRequest:
        bucket: str
        key: str
        data: bytes
        content_type: str = "application/octet-stream"

    @dataclass
    class DownloadRequest:
        bucket: str
        key: str

    @dataclass
    class MetadataRequest:
        bucket: str
        key: str

    @dataclass
    class ListRequest:
        bucket: str
        prefix: str = ""
        delimiter: str = ""
        max_keys: int = 1000

    @staticmethod
    def normalize_upload_response(resp):
        """Convert SDK upload response to a consistent dict format"""
        return {
            "bucket": resp.bucket_name,
            "key": resp.object_key,
            "etag": resp.etag,
            "version_id": getattr(resp, "version_id", None),
        }

    @staticmethod
    def normalize_metadata_response(resp):
        """Extract useful fields from head object response"""
        return {
            "content_type": resp.content_type,
            "size": resp.content_length,
            "last_modified": resp.last_modified.isoformat()
            if resp.last_modified
            else None,
            "etag": resp.etag,
            "storage_class": resp.storage_class,
        }

    @staticmethod
    def normalize_list_response(resp):
        """Flatten SDK list response into a list of simple dicts"""
        contents = getattr(resp, "contents", [])
        return [
            {
                "key": obj.key,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat()
                if obj.last_modified
                else None,
            }
            for obj in contents
        ]
