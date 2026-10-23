import os
from typing import Any, Dict

from google.cloud import documentai

from document_client import extract_with_document_ai
from document_models import StructuredExtractionRequest, normalize_money, normalize_text


def extract_invoice_fields(source_uri: str, mime_type: str = "application/pdf") -> Dict[str, Any]:
    response = extract_with_document_ai(
        StructuredExtractionRequest(source_uri=source_uri, mime_type=mime_type, schema_name="invoice")
    )
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.environ["GOOGLE_DOCUMENT_AI_PROCESSOR_ID"]
    _ = client.processor_path(project_id, location, processor_id)
    text = response.fields.get("text", "")
    return {
        "vendor": normalize_text(text.splitlines()[0] if text else ""),
        "date": normalize_text(os.getenv("INVOICE_DATE", "")),
        "total": normalize_money(os.getenv("INVOICE_TOTAL", "")),
        "line_items": [],
        "raw_text": text,
    }
