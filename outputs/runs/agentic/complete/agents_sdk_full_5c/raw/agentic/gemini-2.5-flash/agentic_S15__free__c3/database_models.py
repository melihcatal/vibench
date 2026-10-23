from typing import Dict, Any, Optional

class Document:
    """Represents a generic document structure."""
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Converts the document object to a dictionary for Firestore."""
        return self.data

    @staticmethod
    def from_firestore_document(doc_id: str, doc_data: Dict[str, Any]) -> 'Document':
        """Creates a Document object from Firestore document data."""
        return Document(id=doc_id, data=doc_data)

class ProductDocument(Document):
    """Represents a product document with specific fields."""
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        price: float,
        category: str,
        tags: Optional[list[str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(id, data if data is not None else {})
        self.data.update({
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "tags": tags if tags is not None else [],
        })

    @property
    def name(self) -> str:
        return self.data.get("name", "")

    @property
    def description(self) -> str:
        return self.data.get("description", "")

    @property
    def price(self) -> float:
        return self.data.get("price", 0.0)

    @property
    def category(self) -> str:
        return self.data.get("category", "")

    @property
    def tags(self) -> list[str]:
        return self.data.get("tags", [])

    @staticmethod
    def from_firestore_document(doc_id: str, doc_data: Dict[str, Any]) -> 'ProductDocument':
        return ProductDocument(
            id=doc_id,
            name=doc_data.get("name", ""),
            description=doc_data.get("description", ""),
            price=doc_data.get("price", 0.0),
            category=doc_data.get("category", ""),
            tags=doc_data.get("tags", []),
            data=doc_data
        )
