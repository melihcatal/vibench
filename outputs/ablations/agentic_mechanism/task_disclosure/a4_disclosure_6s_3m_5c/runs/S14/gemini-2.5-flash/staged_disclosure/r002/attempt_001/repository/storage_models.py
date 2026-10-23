
class StorageRequest:
    def __init__(self, bucket_name: str, object_name: str, region: str = "us-east-1"):
        if not bucket_name:
            raise ValueError("bucket_name cannot be empty")
        if not object_name:
            raise ValueError("object_name cannot be empty")
        self.bucket_name = bucket_name
        self.object_name = self._normalize_object_name(object_name)
        self.region = region

    def _normalize_object_name(self, object_name: str) -> str:
        # Remove leading/trailing slashes
        return object_name.strip('/')

class StorageResponse:
    def __init__(self, success: bool, message: str = "", etag: str = None, last_modified: str = None):
        self.success = success
        self.message = message
        self.etag = etag
        self.last_modified = last_modified

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "etag": self.etag,
            "last_modified": self.last_modified
        }

def normalize_object_name(object_name: str) -> str:
    """
    Normalizes an object name by removing leading and trailing slashes.
    """
    return object_name.strip('/')
