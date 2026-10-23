
from typing import Optional, Dict, Any

class ObjectStorageRequest:
    """Represents a request to a Managed Object Storage service."""
    def __init__(self, operation: str, bucket_name: str, object_name: str, data: Optional[bytes] = None, metadata: Optional[Dict[str, str]] = None):
        self.operation = operation
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.data = data
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return (f"ObjectStorageRequest(operation='{self.operation}', bucket_name='{self.bucket_name}', "
                f"object_name='{self.object_name}', data_present={self.data is not None}, metadata={self.metadata})")

class ObjectStorageResponse:
    """Represents a response from a Managed Object Storage service."""
    def __init__(self, status: str, message: str, data: Optional[bytes] = None, metadata: Optional[Dict[str, str]] = None):
        self.status = status
        self.message = message
        self.data = data
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return (f"ObjectStorageResponse(status='{self.status}', message='{self.message}', "
                f"data_present={self.data is not None}, metadata={self.metadata})")

def normalize_object_name(object_name: str) -> str:
    """
    Normalizes an object name for consistency across different storage providers.
    For now, this simply strips leading/trailing slashes.
    More complex normalization (e.g., character replacement, casing) can be added here.
    """
    return object_name.strip('/')

def create_success_response(message: str = "Operation successful", data: Optional[bytes] = None, metadata: Optional[Dict[str, str]] = None) -> ObjectStorageResponse:
    """Helper to create a successful object storage response."""
    return ObjectStorageResponse(status="success", message=message, data=data, metadata=metadata)

def create_error_response(message: str, data: Optional[bytes] = None, metadata: Optional[Dict[str, str]] = None) -> ObjectStorageResponse:
    """Helper to create an error object storage response."""
    return ObjectStorageResponse(status="error", message=message, data=data, metadata=metadata)
