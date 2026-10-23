from typing import Any, Dict

class StorageRequest:
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)

class StorageResponse:
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}