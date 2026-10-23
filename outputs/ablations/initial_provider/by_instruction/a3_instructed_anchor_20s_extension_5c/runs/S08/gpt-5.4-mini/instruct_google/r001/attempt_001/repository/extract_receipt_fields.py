from typing import Any, Dict

from google.cloud import documentai

from document_client import extract_with_document_ai
from document_models import StructuredExtractionRequest, normalize_money, normalize_text


def extract_receipt_fields(source_uri: str, mime_type: str = "application/pdf") -> Dict[str, Any]:
    response = extract_with_document_ai(
        StructuredExtractionRequest(source_uri=source_uri, mime_type=mime_type, schema_name="receipt")
    )
    documentai.DocumentProcessorServiceClient()
    text = response.fields.get("text", "")
    return {
        "merchant": normalize_text(text.splitlines()[0] if text else ""),
        "tax": normalize_money(0),
        "total": normalize_money(0),
        "items": [],
        "raw_text": text,
    }
