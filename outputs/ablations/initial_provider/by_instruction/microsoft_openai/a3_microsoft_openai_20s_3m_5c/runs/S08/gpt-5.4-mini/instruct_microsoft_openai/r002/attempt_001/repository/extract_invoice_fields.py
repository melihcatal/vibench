from document_client import extract_structured_document
from document_models import StructuredDocumentRequest


PROMPT = "Extract invoice vendor, date, total, and line items as JSON with confidence fields using OpenAI structured extraction."


def extract_invoice_fields(document_text: str):
    request = StructuredDocumentRequest(document_text=document_text, document_type="invoice")
    return extract_structured_document(PROMPT, request)
