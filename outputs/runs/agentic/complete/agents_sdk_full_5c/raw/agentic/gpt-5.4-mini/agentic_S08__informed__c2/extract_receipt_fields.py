from __future__ import annotations

from typing import Any, Dict

from document_client import StructuredDocumentClient
from document_models import DocumentExtractionRequest


def extract_receipt_fields(file_path: str, processor_id: str | None = None) -> Dict[str, Any]:
    client = StructuredDocumentClient(processor_id=processor_id)
    response = client.process_document(DocumentExtractionRequest(file_path=file_path, processor_id=processor_id, mime_type="application/pdf"))
    return {
        "merchant": response.merchant or response.vendor,
        "tax": response.tax,
        "total": response.total,
        "items": [item.to_dict() for item in response.line_items],
        "raw": response.raw,
    }
