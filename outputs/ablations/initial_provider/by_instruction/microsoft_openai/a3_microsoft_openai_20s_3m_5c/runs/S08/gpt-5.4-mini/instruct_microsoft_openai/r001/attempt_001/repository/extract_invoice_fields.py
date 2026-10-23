from document_client import extract_structured_document
from document_models import DocumentRequest


def extract_invoice_fields(document_text: str):
    request = DocumentRequest(document_text=document_text, document_type="invoice")
    response = extract_structured_document(request, "invoice_fields")
    fields = response.fields
    return {
        "vendor": fields.get("vendor"),
        "date": fields.get("date"),
        "total": fields.get("total"),
        "line_items": fields.get("line_items", []),
        "confidences": response.confidences,
    }
