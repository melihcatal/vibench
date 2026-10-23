from typing import Optional, Dict, Any


class StorageObject:
    def __init__(
        self, bucket_name: str, object_key: str, content_type: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.content_type = content_type


class UploadResponse:
    def __init__(self, etag: str, version_id: Optional[str] = None):
        self.etag = etag
        self.version_id = version_id


class PresignedUrlResponse:
    def __init__(self, url: str):
        self.url = url


class ObjectMetadataResponse:
    def __init__(
        self, metadata: Dict[str, Any], content_length: int, last_modified: Any
    ):
        self.metadata = metadata
        self.content_length = content_length
        self.last_modified = last_modified


class ListObjectsResponse:
    def __init__(
        self,
        objects: list[Dict[str, Any]],
        next_continuation_token: Optional[str] = None,
    ):
        self.objects = objects
        self.next_continuation_token = next_continuation_token
