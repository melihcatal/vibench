from typing import Dict


class StorageObject:
    def __init__(self, bucket_name: str, key: str, metadata: Dict):
        self.bucket_name = bucket_name
        self.key = key
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data["bucket_name"], data["key"], data["metadata"])
