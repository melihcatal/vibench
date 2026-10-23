import json
from typing import Any, Dict, List, Optional


class Document:
    def __init__(self, id: str, content: Dict[str, Any]):
        self.id = id
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        return {"_id": self.id, **self.content}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Document":
        doc_id = data.pop("_id")
        return Document(id=str(doc_id), content=data)


class DocumentQuery:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value


class DocumentUpdate:
    def __init__(self, id: str, updates: Dict[str, Any], version: Optional[int] = None):
        self.id = id
        self.updates = updates
        self.version = version
