from typing import Dict, Any


class Document:
    """A simple model for a document in the NoSQL store."""

    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self):
        return self.data

    @classmethod
    def from_dict(cls, id: str, source: Dict[str, Any]):
        return cls(id, source)
