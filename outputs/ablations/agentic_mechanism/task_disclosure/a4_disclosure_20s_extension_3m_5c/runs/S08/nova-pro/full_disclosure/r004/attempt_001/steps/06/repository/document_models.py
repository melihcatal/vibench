from typing import Any, Dict, List

class DocumentRequest:
    def __init__(self, document_id: str, document_type: str):
        self.document_id = document_id
        self.document_type = document_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            'document_id': self.document_id,
            'document_type': self.document_type
        }

class DocumentResponse:
    def __init__(self, document_id: str, extracted_fields: Dict[str, Any]):
        self.document_id = document_id
        self.extracted_fields = extracted_fields

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentResponse':
        return cls(
            document_id=data['document_id'],
            extracted_fields=data['extracted_fields']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'document_id': self.document_id,
            'extracted_fields': self.extracted_fields
        }

def normalize_document_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized_fields = {}
    for key, value in extracted_fields.items():
        normalized_fields[key.lower()] = value
    return normalized_fields