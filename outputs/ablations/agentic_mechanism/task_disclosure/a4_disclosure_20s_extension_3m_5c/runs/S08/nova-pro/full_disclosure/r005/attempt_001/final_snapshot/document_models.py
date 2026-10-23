from typing import List, Dict, Any

class DocumentRequest:
    def __init__(self, document_type: str, document_content: str):
        self.document_type = document_type
        self.document_content = document_content

class DocumentResponse:
    def __init__(self, success: bool, extracted_data: Dict[str, Any]):
        self.success = success
        self.extracted_data = extracted_data

def normalize_document_data(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    normalized_data = {}
    for key, value in extracted_data.items():
        normalized_data[key.lower().replace(' ', '_')] = value
    return normalized_data