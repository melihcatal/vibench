from typing import Optional, Dict, Any

class StorageObject:
    def __init__(self, bucket_name: str, object_name: str, content_type: Optional[str] = None, metadata: Optional[Dict[str, str]] = None):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.content_type = content_type
        self.metadata = metadata

class UploadObjectResponse:
    def __init__(self, etag: str, version_id: Optional[str] = None):
        self.etag = etag
        self.version_id = version_id

class PresignedUrlResponse:
    def __init__(self, url: str):
        self.url = url

class ObjectMetadataResponse:
    def __init__(self, content_type: str, content_length: int, last_modified: Any, etag: str, metadata: Dict[str, str]):
        self.content_type = content_type
        self.content_length = content_length
        self.last_modified = last_modified
        self.etag = etag
        self.metadata = metadata

class ListedObject:
    def __init__(self, object_name: str, last_modified: Any, etag: str, size: int):
        self.object_name = object_name
        self.last_modified = last_modified
        self.etag = etag
        self.size = size

class ListPrefixResponse:
    def __init__(self, objects: list[ListedObject], common_prefixes: list[str]):
        self.objects = objects
        self.common_prefixes = common_prefixes
