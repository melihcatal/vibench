import json
from typing import Any, Dict, Optional, List

class Document:
    def __init__(self, id: str, content: Dict[str, Any], partition_key: Optional[str] = None):
        self.id = id
        self.content = content
        self.partition_key = partition_key

    def to_dict(self) -> Dict[str, Any]:
        doc = {"id": self.id, **self.content}
        if self.partition_key:
            doc["partition_key"] = self.partition_key
        return doc

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Document':
        doc_id = data.pop("id")
        partition_key = data.pop("partition_key", None)
        return Document(id=doc_id, content=data, partition_key=partition_key)

class QueryResult:
    def __init__(self, documents: List[Document], continuation_token: Optional[str] = None):
        self.documents = documents
        self.continuation_token = continuation_token
