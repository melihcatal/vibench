from typing import Any, Dict

class DocumentModel:
    """Simple wrapper for a NoSQL document with typed fields and serialization helpers.
    """
    def __init__(self, doc_id: str, **kwargs: Any):
        self.id = doc_id
        # Store all extra fields in a dict for easy JSON conversion
        self.data: Dict[str, Any] = kwargs

    @classmethod
    def from_dict(cls, source: Dict[str, Any]) -> 'DocumentModel':
        # Assume 'id' is the unique identifier field
        doc_id = source.get('id', str(id(source)))
        kwargs = {k: v for k, v in source.items() if k != 'id'}
        return cls(doc_id, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return {**self.data, 'id': self.id}

    def __repr__(self) -> str:
        return f"DocumentModel(id={self.id}, data={self.data})"
