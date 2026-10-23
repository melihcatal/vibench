from typing import Any, Dict, List, Union

class DocumentRequest:
    def __init__(self, document_id: str, fields: List[str]):
        self.document_id = document_id
        self.fields = fields

    def to_dict(self) -> Dict[str, Any]:
        return {'document_id': self.document_id, 'fields': self.fields}

class DocumentResponse:
    def __init__(self, document_id: str, data: Dict[str, Any]):
        self.document_id = document_id
        self.data = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentResponse':
        return cls(data['document_id'], data['data'])

    def to_dict(self) -> Dict[str, Any]:
        return {'document_id': self.document_id, 'data': self.data}

def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized_document = {}
    for key, value in document.items():
        if isinstance(value, str):
            normalized_document[key] = value.strip()
        elif isinstance(value, list):
            normalized_document[key] = [item.strip() for item in value]
        else:
            normalized_document[key] = value
    return normalized_document