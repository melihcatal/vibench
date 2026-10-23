from typing import Dict, Any, Optional

class Document:
    """Represents a generic document structure with ID and data."""
    def __init__(self, document_id: str, data: Dict[str, Any]):
        self.document_id = document_id
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Converts the document object to a dictionary."""
        return {"id": self.document_id, **self.data}

    @classmethod
    def from_dict(cls, doc_id: str, data: Dict[str, Any]):
        """Creates a Document object from a dictionary."""
        return cls(doc_id, data)

class UpsertResponse:
    """Represents the response of an upsert operation."""
    def __init__(self, success: bool, document_id: str, message: Optional[str] = None):
        self.success = success
        self.document_id = document_id
        self.message = message

    def to_dict(self):
        return {"success": self.success, "document_id": self.document_id, "message": self.message}

class FetchResponse:
    """Represents the response of a fetch operation."""
    def __init__(self, success: bool, document: Optional[Document] = None, message: Optional[str] = None):
        self.success = success
        self.document = document
        self.message = message

    def to_dict(self):
        result = {"success": self.success}
        if self.document:
            result["document"] = self.document.to_dict()
        if self.message:
            result["message"] = self.message
        return result

class QueryResponse:
    """Represents the response of a query operation."""
    def __init__(self, success: bool, documents: list[Document], message: Optional[str] = None):
        self.success = success
        self.documents = documents
        self.message = message

    def to_dict(self):
        return {
            "success": self.success,
            "documents": [doc.to_dict() for doc in self.documents],
            "message": self.message
        }

if __name__ == '__main__':
    # Example usage:
    doc_data = {"name": "Example Doc", "value": 42}
    my_doc = Document("doc_abc", doc_data)
    print(my_doc.to_dict())

    upsert_res = UpsertResponse(True, "doc_abc", "Document created.")
    print(upsert_res.to_dict())

    fetch_res = FetchResponse(True, my_doc)
    print(fetch_res.to_dict())

    query_res = QueryResponse(True, [my_doc])
    print(query_res.to_dict())
