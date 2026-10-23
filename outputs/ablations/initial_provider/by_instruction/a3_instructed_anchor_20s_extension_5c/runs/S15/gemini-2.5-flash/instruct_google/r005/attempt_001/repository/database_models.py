import dataclasses
from typing import Any, Dict

@dataclasses.dataclass
class Document:
    id: str
    data: Dict[str, Any]

    def to_dict(self):
        return self.data

    @staticmethod
    def from_dict(doc_id: str, source: Dict[str, Any]):
        return Document(id=doc_id, data=source)
