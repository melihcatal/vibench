import json
from typing import Dict, Any, Optional

class DocumentData:
    """A simple model for document data."""
    def __init__(self, id: str, content: Dict[str, Any], version: Optional[int] = 1):
        self.id = id
        self.content = content
        self.version = version

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data.get("id"), data.get("content", {}), data.get("version"))

class DocumentResponse:
    """Standardized response structure for document operations."""
    def __init__(self, status: str, message: Optional[str] = None, data: Optional[Dict[str, Any]] = None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

# Example usage (not part of the core integration logic)
if __name__ == '__main__':
    doc_content = {"title": "My Doc", "text": "Hello World"}
    doc = DocumentData(id="doc1", content=doc_content)
    print(f"DocumentData: {doc.to_dict()}")

    response = DocumentResponse(status="success", data=doc.to_dict())
    print(f"DocumentResponse: {response.to_dict()}")
