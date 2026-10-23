from typing import Dict, Any, Optional


class Document:
    def __init__(
        self, document_id: str, content: Dict[str, Any], version: Optional[int] = None
    ):
        self.document_id = document_id
        self.content = content
        self.version = version

    def to_dict(self):
        doc_dict = {"_id": self.document_id, "content": self.content}
        if self.version is not None:
            doc_dict["version"] = self.version
        return doc_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data["_id"], data["content"], data.get("version"))


class QueryResult:
    def __init__(self, documents: list[Document]):
        self.documents = documents

    def to_list_of_dicts(self):
        return [doc.to_dict() for doc in self.documents]
