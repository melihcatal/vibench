from typing import Any, Dict, List


class DocumentRequest:
    def __init__(self, document_id: str, fields: List[str]):
        self.document_id = document_id
        self.fields = fields

    def to_dict(self) -> Dict[str, Any]:
        return {
            'document_id': self.document_id,
            'fields': self.fields,
        }


class DocumentResponse:
    def __init__(self, document_id: str, data: Dict[str, Any]):
        self.document_id = document_id
        self.data = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentResponse':
        return cls(
            document_id=data['document_id'],
            data=data['data'],
        )


def normalize_document_data(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            normalized_data[key] = value.strip()
        else:
            normalized_data[key] = value
    return normalized_data