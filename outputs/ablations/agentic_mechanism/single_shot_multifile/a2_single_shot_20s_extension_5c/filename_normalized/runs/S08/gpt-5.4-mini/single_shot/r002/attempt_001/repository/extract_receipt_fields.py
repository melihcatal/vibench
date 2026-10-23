import os
from typing import Any, Dict, Optional

from document_client import get_extraction_client
from document_models import DocumentExtractionRequest, normalize_document_text

MODEL_ID = os.getenv("OPENAI_RECEIPT_MODEL", "gpt-4.1-mini")


def extract_receipt_fields(document_text: str, *, file_name: Optional[str] = None, mime_type: Optional[str] = None, confidence_threshold: float = 0.0) -> Dict[str, Any]:
    client = get_extraction_client()
    request = DocumentExtractionRequest(document_type="receipt", text=normalize_document_text(document_text), file_name=file_name, mime_type=mime_type, confidence_threshold=confidence_threshold)
    return client.extract_with_openai(model=MODEL_ID, request=request, schema_name="receipt_fields")
