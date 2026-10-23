from typing import Any, Dict, List

class DocumentRequest:
    def __init__(self, document_type: str, document_content: bytes):
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            'extracted_fields': self.extracted_fields,
            'confidence_scores': self.confidence_scores
        }

def normalize_document_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized_fields = {}
    for key, value in extracted_fields.items():
        normalized_fields[key.lower().replace(' ', '_')] = value
    return normalized_fields