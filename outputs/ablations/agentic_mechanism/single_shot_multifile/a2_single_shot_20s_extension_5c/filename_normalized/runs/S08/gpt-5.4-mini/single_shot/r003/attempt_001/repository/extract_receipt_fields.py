from document_client import create_document_ai_client, extract_structured_fields
from document_models import StructuredDocumentRequest, coerce_receipt_extraction


def extract_receipt_fields(text: str, document_id: str | None = None) -> dict:
    client = create_document_ai_client()
    request = StructuredDocumentRequest(document_type="receipt", text=text, document_id=document_id)
    response = extract_structured_fields(client, request, model="gemini-1.5-pro")
    return coerce_receipt_extraction(response)
