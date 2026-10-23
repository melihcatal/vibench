from typing import Dict, Any, Optional


class Document:
    def __init__(self, id: str, content: Dict[str, Any], etag: Optional[str] = None):
        self.id = id
        self.content = content
        self.etag = etag

    def to_dict(self):
        doc_dict = {"id": self.id, **self.content}
        if self.etag:
            doc_dict["_etag"] = self.etag
        return doc_dict

    @staticmethod
    def from_dict(doc_dict: Dict[str, Any]):
        doc_id = doc_dict.pop("id")
        etag = doc_dict.pop("_etag", None)
        return Document(id=doc_id, content=doc_dict, etag=etag)
