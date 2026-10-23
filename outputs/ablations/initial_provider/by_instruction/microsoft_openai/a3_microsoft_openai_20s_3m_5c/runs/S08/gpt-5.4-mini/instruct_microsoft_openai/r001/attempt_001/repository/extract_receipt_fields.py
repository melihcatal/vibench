from document_client import extract_structured_document
from document_models import DocumentRequest


def extract_receipt_fields(document_text: str):
    request = DocumentRequest(document_text=document_text, document_type="receipt")
    response = extract_structured_document(request, "receipt_fields")
    fields = response.fields
    return {
        "merchant": fields.get("merchant"),
        "tax": fields.get("tax"),
        "total": fields.get("total"),
        "items": fields.get("items", []),
        "confidences": response.confidences,
    }
