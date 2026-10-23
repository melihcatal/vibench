from document_client import create_document_ai_client, extract_structured_fields
from document_models import StructuredDocumentRequest, coerce_invoice_extraction


def extract_invoice_fields(text: str, document_id: str | None = None) -> dict:
    client = create_document_ai_client()
    request = StructuredDocumentRequest(document_type="invoice", text=text, document_id=document_id)
    response = extract_structured_fields(client, request, model="gemini-1.5-pro")
    return coerce_invoice_extraction(response)
