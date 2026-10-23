from typing import Any, Dict, List

class DocumentRequest:
    def __init__(self, document_type: str, document_content: str):
        self.document_type = document_type
        self.document_content = document_content

    def to_dict(self) -> Dict[str, Any]:
        return {
            'document_type': self.document_type,
            'document_content': self.document_content
        }


class DocumentResponse:
    def __init__(self, extracted_fields: Dict[str, Any], confidence_scores: Dict[str, float]):
        self.extracted_fields = extracted_fields
        self.confidence_scores = confidence_scores

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            extracted_fields=data['extracted_fields'],
            confidence_scores=data['confidence_scores']
        )


def normalize_document_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized_fields = {}
    for field, value in extracted_fields.items():
        normalized_fields[field.lower()] = value
    return normalized_fields
