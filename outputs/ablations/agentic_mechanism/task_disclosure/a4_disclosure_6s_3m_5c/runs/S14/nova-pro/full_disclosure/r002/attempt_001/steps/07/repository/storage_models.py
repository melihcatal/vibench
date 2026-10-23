from typing import Any, Dict, List, Union


class StorageRequest:
    def __init__(self, bucket: str, key: str, metadata: Dict[str, Any] = None):
        self.bucket = bucket
        self.key = key
        self.metadata = metadata or {}


class StorageResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: Union[str, bytes]):
        self.status_code = status_code
        self.headers = headers
        self.body = body


def normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, str]:
    return {k: str(v) for k, v in metadata.items()}


def normalize_response(response: StorageResponse) -> Dict[str, Any]:
    return {
        'status_code': response.status_code,
        'headers': response.headers,
        'body': response.body.decode() if isinstance(response.body, bytes) else response.body
    }