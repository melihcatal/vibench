from typing import Dict, Any, Optional


class Document:
    """Represents a document in the NoSQL store."""

    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self):
        return {"id": self.id, "data": self.data}


class DocumentId:
    """Represents a document identifier."""

    def __init__(self, id: str):
        self.id = id
