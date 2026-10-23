from typing import Dict, Any


class StorageResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @staticmethod
    def normalize(response: Dict[str, Any]) -> 'StorageResponse':
        return StorageResponse(response)