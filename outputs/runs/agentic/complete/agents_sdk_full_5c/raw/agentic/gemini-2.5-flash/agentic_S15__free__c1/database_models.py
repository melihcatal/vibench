from typing import Dict, Any, Optional

class Document:
    """Base class for a document in the NoSQL store."""
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, **self.data}

    @classmethod
    def from_dict(cls, doc_id: str, data: Dict[str, Any]):
        return cls(doc_id, data)

class ProductDocument(Document):
    """Example: A product document with specific fields."""
    def __init__(self, id: str, name: str, description: str, price: float, sku: str, version: Optional[int] = 1, **kwargs):
        super().__init__(id, {
            "name": name,
            "description": description,
            "price": price,
            "sku": sku,
            "version": version,
            **kwargs
        })
        self.name = name
        self.description = description
        self.price = price
        self.sku = sku
        self.version = version

    @classmethod
    def from_dict(cls, doc_id: str, data: Dict[str, Any]):
        return cls(
            id=doc_id,
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            sku=data.get("sku"),
            version=data.get("version", 1),
            **{k: v for k, v in data.items() if k not in ["name", "description", "price", "sku", "version"]}
        )
