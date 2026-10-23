
class StorageRequest:
    """Represents a request to the Managed Object Storage."""
    def __init__(self, bucket_name: str, object_key: str, data: bytes = None):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.data = data

class StorageResponse:
    """Represents a response from the Managed Object Storage."""
    def __init__(self, success: bool, message: str = "", data: bytes = None):
        self.success = success
        self.message = message
        self.data = data

def normalize_object_key(key: str) -> str:
    """Normalizes an object key for Managed Object Storage.

    This example simply strips leading/trailing slashes and ensures no double slashes.
    In a real-world scenario, this might involve more complex logic based on
    the specific object storage provider's requirements.
    """
    normalized_key = key.strip('/')
    normalized_key = '/'.join(filter(None, normalized_key.split('/')))
    return normalized_key
