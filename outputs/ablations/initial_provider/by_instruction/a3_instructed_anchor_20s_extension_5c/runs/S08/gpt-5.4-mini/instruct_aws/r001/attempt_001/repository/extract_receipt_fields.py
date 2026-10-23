from document_client import DocumentClient
from document_models import DocumentExtractionRequest


def extract_receipt_fields(document_uri: str):
    client = DocumentClient()
    response = client.analyze_document(DocumentExtractionRequest(document_uri=document_uri, document_type="receipt"))
    return {
        "merchant": response.fields.get("merchant_name") or response.fields.get("vendor_name"),
        "tax": response.fields.get("tax"),
        "total": response.fields.get("total"),
        "items": response.fields.get("line_items", []),
        "confidence": response.confidences,
        "provider": response.provider,
    }
