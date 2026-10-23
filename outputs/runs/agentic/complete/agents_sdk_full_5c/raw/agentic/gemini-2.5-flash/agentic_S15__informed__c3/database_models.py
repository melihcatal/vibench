from typing import Optional, Dict, Any

class DocumentData:
    """
    A simple model for document data.
    """
    def __init__(self, doc_id: str, data: Dict[str, Any], version: Optional[int] = None):
        self.doc_id = doc_id
        self.data = data
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        if self.version is not None:
            return {**self.data, "_version": self.version}
        return self.data

    @classmethod
    def from_dict(cls, doc_id: str, data: Dict[str, Any]):
        version = data.pop("_version", None)
        return cls(doc_id=doc_id, data=data, version=version)

