from typing import Any, Dict


class StorageRequest:
    def __init__(self, data: Any, content_type: str = 'application/octet-stream'):
        self.data = data
        self.content_type = content_type


class StorageResponse:
    def __init__(self, data: Dict):
        self.data = data


def normalize_payload(payload: Dict) -> StorageRequest:
    return StorageRequest(payload['data'], payload.get('content_type', 'application/octet-stream'))


def normalize_response(response: Dict) -> StorageResponse:
    return StorageResponse(response)