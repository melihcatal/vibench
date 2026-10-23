from typing import Any, Dict, List

class DocumentRequest:
    def __init__(self, document_type: str, document_content: str):
        self.document_type = document_type
        self.document_content = document_content

class DocumentResponse:
    def __init__(self, document_type: str, extracted_fields: Dict[str, Any]):
        self.document_type = document_type
        self.extracted_fields = extracted_fields

def normalize_document_fields(document_type: str, extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized_fields = {}
    if document_type == 'invoice':
        normalized_fields['vendor'] = extracted_fields.get('vendor', '')
        normalized_fields['date'] = extracted_fields.get('date', '')
        normalized_fields['total'] = extracted_fields.get('total', 0)
        normalized_fields['line_items'] = extracted_fields.get('line_items', [])
    elif document_type == 'receipt':
        normalized_fields['merchant'] = extracted_fields.get('merchant', '')
        normalized_fields['tax'] = extracted_fields.get('tax', 0)
        normalized_fields['total'] = extracted_fields.get('total', 0)
        normalized_fields['items'] = extracted_fields.get('items', [])
    return normalized_fields