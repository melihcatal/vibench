import os

from document_client import extract_structured_document
from document_models import DocumentSource, StructuredDocumentRequest


def extract_invoice_fields(path: str):
    schema = {
        "type": "object",
        "properties": {
            "vendor": {"type": "string"},
            "date": {"type": "string"},
            "total": {"type": "number"},
            "line_items": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["vendor", "date", "total", "line_items"],
    }
    request = StructuredDocumentRequest(document=DocumentSource(path=path), schema_name="invoice", schema=schema, model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    return extract_structured_document(request)
