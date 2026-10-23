# Request/response and normalization helpers for Managed Object Storage


class ObjectMetadata:
    """Container for object metadata fields returned by storage API."""

    def __init__(self, name: str, size: int, last_modified: str, content_type: str):
        self.name = name
        self.size = size
        self.last_modified = last_modified
        self.content_type = content_type


class PutObjectRequest:
    """Payload for uploading a file or bytes to storage."""

    def __init__(self, bucket: str, key: str, body: bytes):
        self.bucket = bucket
        self.key = key
        self.body = body


class GetObjectResponse:
    """Response wrapper for downloaded object data."""

    def __init__(self, body: bytes, metadata: dict):
        self.body = body  # bytes of file content
        self.metadata = metadata  # dict with metadata fields
