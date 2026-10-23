from typing import Any, Dict

class StorageRequest:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return self.kwargs

class StorageResponse:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return self.kwargs