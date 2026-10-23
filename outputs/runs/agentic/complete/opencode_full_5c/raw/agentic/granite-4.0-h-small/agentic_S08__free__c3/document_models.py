from typing import List, Dict, Any

# Define common request/response shapes that any provider can map to.

PurchaseItem = Dict[str, Any]  # Generic item entry (name/description, qty, unit price)

InvoiceRequest = Dict[str, Any]
InvoiceResponse = Dict[str, Any]
ReceiptRequest = Dict[str, Any]
ReceiptResponse = Dict[str, Any]

# Helper to construct request dicts that can be sent to providers.


def build_invoice_request(pdf_bytes: bytes) -> InvoiceRequest:
    """Placeholder helper – in practice this could add OCR hints, page ranges, etc.","""
    return {"documentBytes": pdf_bytes, "documentType": "invoice"}


HEADER = {"Ocp-Apim-Subscription-Key": os.getenv("AZURE_FORM_RECOGNIZER_KEY")}


def build_receipt_request(image_bytes: bytes) -> ReceiptRequest:
    """Placeholder helper for receipt extraction.","""
    return {"documentBytes": image_bytes, "documentType": "receipt"}
