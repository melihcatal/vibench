from document_client import DocumentClient
from document_models import DocumentExtractionRequest


def extract_invoice_fields(document_uri: str):
    client = DocumentClient()
    response = client.analyze_document(DocumentExtractionRequest(document_uri=document_uri, document_type="invoice"))
    return {
        "vendor": response.fields.get("vendor_name") or response.fields.get("vendor"),
        "date": response.fields.get("invoice_receipt_date") or response.fields.get("date"),
        "total": response.fields.get("total") or response.fields.get("amount_due"),
        "line_items": response.fields.get("line_items", []),
        "confidence": response.confidences,
        "provider": response.provider,
    }
