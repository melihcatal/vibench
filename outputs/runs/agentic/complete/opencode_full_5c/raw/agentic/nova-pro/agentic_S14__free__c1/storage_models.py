from typing import Any, Dict


class S3Object:
    def __init__(self, key: str, metadata: Dict[str, Any]):
        self.key = key
        self.metadata = metadata

    @staticmethod
    def from_response(response: Dict[str, Any]):
        return S3Object(response["Key"], response["Metadata"])
