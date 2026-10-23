from typing import Dict, Any, Optional

class Document:
    """A simple class to represent a document with basic properties."""
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Converts the document object to a dictionary."""
        return {"id": self.id, **self.data}

    @classmethod
    def from_dict(cls, doc_id: str, source: Dict[str, Any]):
        """Creates a Document object from a dictionary."""
        return cls(doc_id, source)


class DocumentQueryResponse:
    """Represents a response from a document query operation."""
    def __init__(self, documents: list[Document], total_count: int):
        self.documents = documents
        self.total_count = total_count

    def to_list_of_dicts(self) -> list[Dict[str, Any]]:
        return [doc.to_dict() for doc in self.documents]


# Example usage for normalization (optional, can be done inline as well)
def normalize_document_for_storage(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes incoming data before storing it in the database."""
    # Example: ensure all names are capitalized, add a timestamp, etc.
    if "name" in raw_data and isinstance(raw_data["name"], str):
        raw_data["name"] = raw_data["name"].capitalize()
    # raw_data["last_updated"] = datetime.utcnow().isoformat() # Requires import datetime
    return raw_data

def parse_document_from_db(doc_id: str, db_data: Dict[str, Any]) -> Document:
    """Parses raw database output into a standardized Document object."""
    return Document.from_dict(doc_id, db_data)
