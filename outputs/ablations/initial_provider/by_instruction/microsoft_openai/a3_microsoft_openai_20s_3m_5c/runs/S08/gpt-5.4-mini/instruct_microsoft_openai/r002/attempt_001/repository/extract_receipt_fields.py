from document_client import extract_structured_document
from document_models import StructuredDocumentRequest


PROMPT = "Extract receipt merchant, tax, total, and items as JSON with confidence fields using OpenAI structured extraction."


def extract_receipt_fields(document_text: str):
    request = StructuredDocumentRequest(document_text=document_text, document_type="receipt")
    return extract_structured_document(PROMPT, request)
