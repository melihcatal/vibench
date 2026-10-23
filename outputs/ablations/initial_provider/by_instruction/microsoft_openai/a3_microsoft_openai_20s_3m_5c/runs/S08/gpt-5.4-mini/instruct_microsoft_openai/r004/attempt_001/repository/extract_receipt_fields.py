import os

from document_client import extract_structured_document
from document_models import DocumentSource, StructuredDocumentRequest


def extract_receipt_fields(path: str):
    schema = {"type": "object", "properties": {"merchant": {"type": "string"}, "tax": {"type": "number"}, "total": {"type": "number"}, "items": {"type": "array", "items": {"type": "object"}}}, "required": ["merchant", "tax", "total", "items"]}
    request = StructuredDocumentRequest(document=DocumentSource(path=path), schema_name="receipt", schema=schema, model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    return extract_structured_document(request)
