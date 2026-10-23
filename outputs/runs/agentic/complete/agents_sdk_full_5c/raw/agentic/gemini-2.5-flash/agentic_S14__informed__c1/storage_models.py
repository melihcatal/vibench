from typing import List, Dict, Any

# This file can be extended to include pydantic models or dataclasses
# for more structured request/response objects related to storage operations.
# For now, simple type hints are used directly in function signatures.

class StorageObjectMetadata:
    """
    A placeholder class to represent normalized object metadata.
    """
    def __init__(self, key: str, size: int, last_modified: str, etag: str, custom_metadata: Dict[str, str]):
        self.key = key
        self.size = size
        self.last_modified = last_modified
        self.etag = etag
        self.custom_metadata = custom_metadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "size": self.size,
            "last_modified": self.last_modified,
            "etag": self.etag,
            "custom_metadata": self.custom_metadata,
        }

