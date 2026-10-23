from typing import Optional, Dict, Any

class StorageUploadRequest:
    object_name: str
    data: Any
    content_type: Optional[str] = "application/octet-stream"

    def __init__(self, object_name: str, data: Any, content_type: Optional[str] = None):
        self.object_name = object_name
        self.data = data
        if content_type:
            self.content_type = content_type

class StorageObjectMetadata:
    name: str
    size: int
    creation_time: str
    last_modified_time: str
    content_type: str
    etag: str
    metadata: Optional[Dict[str, str]]

    def __init__(self, name: str, size: int, creation_time: str, last_modified_time: str, content_type: str, etag: str, metadata: Optional[Dict[str, str]] = None):
        self.name = name
        self.size = size
        self.creation_time = creation_time
        self.last_modified_time = last_modified_time
        self.content_type = content_type
        self.etag = etag
        self.metadata = metadata or {}

class StoragePresignedUrlResponse:
    object_name: str
    presigned_url: str

    def __init__(self, object_name: str, presigned_url: str):
        self.object_name = object_name
        self.presigned_url = presigned_url

class StorageObjectListing:
    object_name: str
    size: int
    last_modified_time: str
    etag: str

    def __init__(self, object_name: str, size: int, last_modified_time: str, etag: str):
        self.object_name = object_name
        self.size = size
        self.last_modified_time = last_modified_time
        self.etag = etag
