from typing import Dict, Any

class Document:
    """
    A simple model for a document in the NoSQL store.
    """
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Document object to a dictionary suitable for storage.
        """
        return {"id": self.id, **self.data}

    @classmethod
    def from_dict(cls, doc_id: str, source: Dict[str, Any]):
        """
        Creates a Document object from a dictionary retrieved from the store.
        """
        data = {k: v for k, v in source.items() if k != 'id'}
        return cls(doc_id, data)
