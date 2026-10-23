from typing import Dict, Any, Optional

# This file provides a simple data class for representing documents.
# In a more complex application, this could use libraries like Pydantic
# for validation and serialization.

class Document:
    """A simple class to represent a document stored in the database."""

    def __init__(self, doc_id: str, content: str, author: str, version: int = 1):
        self.doc_id = doc_id
        self.content = content
        self.author = author
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Document object to a dictionary for database storage."""
        return {
            "_id": self.doc_id,
            "content": self.content,
            "author": self.author,
            "_version": self.version,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Optional["Document"]:
        """Creates a Document object from a dictionary retrieved from the database."""
        if not data:
            return None
        return Document(
            doc_id=data.get("_id"),
            content=data.get("content"),
            author=data.get("author"),
            version=data.get("_version", 1),
        )
