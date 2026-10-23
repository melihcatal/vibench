from typing import Dict, Any

class Document:
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_dict(self):
        return dict(self.data, id=self.id)

    @staticmethod
    def from_dict(doc_dict: Dict[str, Any]):
        doc_id = doc_dict.pop('id', None)
        if not doc_id:
            raise ValueError("Document dictionary must contain an 'id' field.")
        return Document(id=doc_id, data=doc_dict)
