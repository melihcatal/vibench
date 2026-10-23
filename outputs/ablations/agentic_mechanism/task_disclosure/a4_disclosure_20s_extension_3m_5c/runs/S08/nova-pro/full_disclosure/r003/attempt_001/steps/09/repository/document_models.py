from typing import Any, Dict, List


class DocumentRequest:
    def __init__(self, document_type: str, document_content: str):
        self.document_type = document_type
        self.document_content = document_content


class DocumentResponse:
    def __init__(self, success: bool, extracted_fields: Dict[str, Any]):
        self.success = success
        self.extracted_fields = extracted_fields


def normalize_document_fields(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized_fields = {}
    for key, value in extracted_fields.items():
        normalized_fields[key.lower()] = value
    return normalized_fields