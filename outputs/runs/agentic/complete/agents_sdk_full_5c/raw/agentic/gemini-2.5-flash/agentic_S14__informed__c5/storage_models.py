from typing import Optional

class StorageObject:
    def __init__(self, bucket_name: str, key: str, content: Optional[bytes] = None, content_type: Optional[str] = None):
        self.bucket_name = bucket_name
        self.key = key
        self.content = content
        self.content_type = content_type

class ObjectMetadata:
    def __init__(self, bucket_name: str, key: str, etag: str, size: int, last_modified: str, content_type: str):
        self.bucket_name = bucket_name
        self.key = key
        self.etag = etag
        self.size = size
        self.last_modified = last_modified
        self.content_type = content_type

class PresignedUrl:
    def __init__(self, url: str, expires_in_seconds: int):
        self.url = url
        self.expires_in_seconds = expires_in_seconds

class ListedObject:
    def __init__(self, key: str, size: int, last_modified: str):
        self.key = key
        self.size = size
        self.last_modified = last_modified
