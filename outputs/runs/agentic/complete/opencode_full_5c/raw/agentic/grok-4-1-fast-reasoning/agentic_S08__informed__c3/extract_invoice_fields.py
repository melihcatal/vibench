import os
from mindee.client import Client
from mindee.product import InvoiceV4


def extract_invoice_fields(pdf_path: str) -> dict:
    """
    Extract structured fields from an invoice PDF using Mindee Invoice OCR.
    Returns dict with vendor, date, total, line_items.
    """
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable is required.")

    client = Client(api_key=api_key)
    source_doc = client.source_from_path(pdf_path)
    api_response = source_doc.parse(InvoiceV4)

    prediction = api_response.document.inference.prediction

    line_items = []
    for item in prediction.line_items or []:
        line_items.append(
            {
                "description": item.description.value or "",
                "quantity": item.quantity.value,
                "unit_price": item.unit_price.value,
                "amount": item.total_amount.value,
            }
        )

    return {
        "vendor": {
            "value": prediction.supplier.name.value or "",
            "confidence": float(prediction.supplier.name.confidence),
        },
        "date": {
            "value": prediction.invoice_date.value or "",
            "confidence": float(prediction.invoice_date.confidence),
        },
        "total": {
            "value": str(prediction.total_amount.value),
            "confidence": float(prediction.total_amount.confidence),
        },
        "line_items": line_items,
    }
