from typing import Dict


class S3Object:
    def __init__(self, key: str, metadata: Dict):
        self.key = key
        self.metadata = metadata
