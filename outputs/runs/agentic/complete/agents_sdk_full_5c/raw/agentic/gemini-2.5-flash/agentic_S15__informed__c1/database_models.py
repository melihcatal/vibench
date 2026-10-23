from typing import Optional, Dict, Any

class Document:
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, **self.data}

    @classmethod
    def from_dict(cls, id: str, data: Dict[str, Any]):
        return cls(id, data)

    def __repr__(self):
        return f"Document(id='{self.id}', data={self.data})"

class DocumentQuery:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {"field": self.field, "value": self.value}

if __name__ == "__main__":
    # Example usage
    doc_data = {"name": "Sample Item", "price": 29.99, "available": True}
    my_document = Document(id="item_123", data=doc_data)
    print(my_document)
    print(my_document.to_dict())

    retrieved_doc_dict = {"id": "item_123", "name": "Sample Item", "price": 29.99, "available": True}
    # For simplicity, assuming 'id' is extracted separately from DB results
    retrieved_doc = Document.from_dict(retrieved_doc_dict.pop("id"), retrieved_doc_dict)
    print(retrieved_doc)

    query = DocumentQuery("available", True)
    print(query.to_dict())
