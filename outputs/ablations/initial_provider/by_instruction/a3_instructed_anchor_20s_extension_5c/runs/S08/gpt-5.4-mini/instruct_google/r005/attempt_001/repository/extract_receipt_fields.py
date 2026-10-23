from typing import Any, Dict

from document_client import load_config, process_document_with_google_document_ai
from document_models import StructuredDocumentRequest


def extract_receipt_fields(request: StructuredDocumentRequest) -> Dict[str, Any]:
    cfg = load_config()
    payload = {
        "rawDocument": {
            "mimeType": request.mime_type,
            "content": request.document_base64,
        },
        "fields": ["merchant", "tax", "total", "items"],
        "metadata": request.metadata,
    }
    result = process_document_with_google_document_ai(payload, cfg)
    return {
        "merchant": result.get("merchant", {"value": None, "confidence": 0.0}),
        "tax": result.get("tax", {"value": None, "confidence": 0.0}),
        "total": result.get("total", {"value": None, "confidence": 0.0}),
        "items": result.get("items", []),
        "provider": "google-document-ai",
    }
