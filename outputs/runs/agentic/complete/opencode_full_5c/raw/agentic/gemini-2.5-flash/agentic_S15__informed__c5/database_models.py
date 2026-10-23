import json
from typing import Dict, Any


class Document:
    def __init__(self, id: str, content: Dict[str, Any], version: int = 1):
        self.id = id
        self.content = content
        self.version = version

    def to_dict(self):
        return {
            "id": self.id,
            "content": json.dumps(self.content),
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data["id"],
            content=json.loads(data["content"]),
            version=data.get("version", 1),
        )
