from typing import Dict, Any


def normalize_document_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'document_bytes': payload['document_bytes'],
        'mime_type': payload['mime_type']
    }


def normalize_document_response(response: Dict[str, Any]) -> Dict[str, Any]:
    documents = []
    for document in response.get('documents', []):
        fields = document.get('fields', {})
        normalized_fields = {key: value['content'] for key, value in fields.items()}
        documents.append(normalized_fields)
    return {'documents': documents}