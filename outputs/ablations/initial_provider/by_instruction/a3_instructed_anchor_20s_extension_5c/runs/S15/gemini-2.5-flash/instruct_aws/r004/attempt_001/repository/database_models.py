from typing import Dict, Any

class Document:
    def __init__(self, id: str, content: Dict[str, Any]):
        self.id = id
        self.content = content

    def to_item(self) -> Dict[str, Any]:
        item = {"id": self.id}
        item.update(self.content)
        return item

    @staticmethod
    def from_item(item: Dict[str, Any]) -> "Document":
        doc_id = item.pop("id")
        return Document(id=doc_id, content=item)
