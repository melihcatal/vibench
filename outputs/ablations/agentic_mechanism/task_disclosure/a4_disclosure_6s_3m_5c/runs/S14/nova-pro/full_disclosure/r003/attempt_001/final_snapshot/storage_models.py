from typing import Any, Dict, List


class StorageRequest:
    def __init__(self, bucket_name: str, object_key: str, metadata: Dict[str, Any] = None):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.metadata = metadata or {}


class StorageResponse:
    def __init__(self, status_code: int, content: Dict[str, Any] = None):
        self.status_code = status_code
        self.content = content or {}


def normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, str]:
    normalized = {}
    for key, value in metadata.items():
        if isinstance(value, str):
            normalized[key] = value
        elif isinstance(value, (int, float)):
            normalized[key] = str(value)
        else:
            normalized[key] = str(value)
    return normalized
