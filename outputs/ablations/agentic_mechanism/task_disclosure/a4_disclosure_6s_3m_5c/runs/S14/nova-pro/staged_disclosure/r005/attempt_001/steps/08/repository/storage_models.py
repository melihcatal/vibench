from typing import Any, Dict, List

class LocalStorageRequest:
    def __init__(self, bucket_name: str, object_key: str, data: bytes):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.data = data

class LocalStorageResponse:
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

def normalize_storage_response(response: LocalStorageResponse) -> Dict[str, Any]:
    return {
        'status_code': response.status_code,
        'message': response.message
    }

def normalize_storage_request(request: LocalStorageRequest) -> Dict[str, Any]:
    return {
        'bucket_name': request.bucket_name,
        'object_key': request.object_key,
        'data': request.data
    }