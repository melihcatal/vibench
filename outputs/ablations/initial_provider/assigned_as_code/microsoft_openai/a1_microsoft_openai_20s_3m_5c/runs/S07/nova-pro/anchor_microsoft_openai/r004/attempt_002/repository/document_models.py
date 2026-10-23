from typing import Dict, Any

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'document_bytes': payload['document_bytes'],
        'mime_type': payload.get('mime_type', 'application/pdf')
    }