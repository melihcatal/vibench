import os
from typing import Any, Dict

from document_client import load_config, process_document_with_google_document_ai
from document_models import StructuredDocumentRequest, normalize_extracted_fields


def extract_invoice_fields(request: StructuredDocumentRequest) -> Dict[str, Any]:
    cfg = load_config()
    payload = {
        "rawDocument": {
            "mimeType": request.mime_type,
            "content": request.document_base64,
        },
        "fields": ["vendor", "date", "total", "line_items"],
        "metadata": request.metadata,
    }
    result = process_document_with_google_document_ai(payload, cfg)
    extracted = {
        "vendor": result.get("vendor", {"value": None, "confidence": 0.0}),
        "date": result.get("date", {"value": None, "confidence": 0.0}),
        "total": result.get("total", {"value": None, "confidence": 0.0}),
        "line_items": result.get("line_items", []),
        "provider": "google-document-ai",
    }
    return normalize_extracted_fields(extracted)


if os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID"):
    DEFAULT_PROVIDER = "google-document-ai"
