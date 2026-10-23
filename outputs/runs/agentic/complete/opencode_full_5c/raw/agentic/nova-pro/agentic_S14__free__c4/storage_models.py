from typing import Dict


class StorageObject:
    def __init__(self, metadata: Dict):
        self.metadata = metadata

    @staticmethod
    def from_response(response):
        return StorageObject(response["Metadata"])
