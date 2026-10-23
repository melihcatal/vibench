# storage_models.py
# Local request, response, and normalization helpers for Managed Object Storage

from typing import Any, Dict


# Example request model for uploading an object
class UploadObjectRequest:
    def __init__(self, bucket: str, key: str, body: Any) -> None:
        self.bucket = bucket
        self.key = key
        self.body = body


# Example normalized response for metadata extraction
class ObjectMetadata:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.etag = data.get("ETag")
        self.last_modified = data.get("LastModified")
        self.content_type = data.get("ContentType")
        # Add other fields as needed

    def __repr__(self) -> str:
        return f"ObjectMetadata(etag={self.etag}, last_modified={self.last_modified})"


# Add more models (e.g., PresignedDownloadRequest, ListObjectsRequest) as required
