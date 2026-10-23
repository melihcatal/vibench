from __future__ import annotations

from typing import Dict, Any

from document_client import StructuredDocumentClient
from document_models import DocumentExtractionRequest


def extract_invoice_fields(file_path: str, processor_id: str | None = None) -> Dict[str, Any]:
    client = StructuredDocumentClient(processor_id=processor_id)
    response = client.process_document(DocumentExtractionRequest(file_path=file_path, processor_id=processor_id, mime_type="application/pdf"))
    return {
        "vendor": response.vendor,
        "date": response.date,
        "total": response.total,
        "line_items": [item.to_dict() for item in response.line_items],
        "confidence": response.confidence,
        "raw": response.raw,
    }
