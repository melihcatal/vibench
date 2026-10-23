
class ManagedStorageRequest:
    """
    Represents a request to the Managed Object Storage.
    """
    def __init__(self, bucket_name: str, object_key: str, data: bytes = None, metadata: dict = None):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.data = data
        self.metadata = metadata if metadata is not None else {}

class ManagedStorageResponse:
    """
    Represents a response from the Managed Object Storage.
    """
    def __init__(self, success: bool, message: str = "", data: bytes = None, metadata: dict = None):
        self.success = success
        self.message = message
        self.data = data
        self.metadata = metadata if metadata is not None else {}

def normalize_object_data(raw_object_data: dict) -> dict:
    """
    Normalizes raw object data received from a storage service into a consistent format.

    Args:
        raw_object_data: A dictionary containing raw object data from the storage service.

    Returns:
        A dictionary with normalized object data, including 'key', 'size', 'last_modified', etc.
    """
    normalized_data = {
        "key": raw_object_data.get("Key"),
        "size": raw_object_data.get("Size"),
        "last_modified": raw_object_data.get("LastModified"),
        "e_tag": raw_object_data.get("ETag"),
        # Add other common fields as needed
    }
    return normalized_data
