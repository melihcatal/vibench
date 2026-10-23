from typing import Dict, Any


class S3ObjectMetadata:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata

    def get(self, key: str) -> Any:
        return self.metadata.get(key, None)