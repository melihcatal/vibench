from typing import Dict, Any


class Document:
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Converts the document to a dictionary, suitable for Firestore."""
        return self.data

    @staticmethod
    def from_firestore(doc_id: str, doc_data: Dict[str, Any]):
        """Creates a Document object from Firestore data."""
        return Document(id=doc_id, data=doc_data)
