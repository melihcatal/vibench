from typing import List, Dict
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, NormalizedExpense

REQUIRED_FIELDS = {
    "invoice": ["vendor", "date", "total"],
    "receipt": ["merchant", "total"]
}

def validate_document_fields(doc_type: str, response: InvoiceExtractionResponse | ReceiptExtractionResponse) -> bool:
    fields = REQUIRED_FIELDS.get(doc_type, [])
    missing = [f for f in fields if getattr(response, f) is None or getattr(response, f) == ""]
    if missing:
        raise ValueError(f"Missing required fields {missing} in {doc_type} extraction")
    # Simple confidence check - assume the provider returns confidence scores in a dict
    # Not implemented here; placeholder for future validation
    return True
