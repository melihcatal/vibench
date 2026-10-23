from typing import Dict, Any
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense


def validate_document_fields(
    document_type: str, extracted_data: Dict[str, Any], min_confidence: float = 0.7
) -> Dict[str, Any]:
    errors = []
    confidence = extracted_data.get("confidence", 0.0)

    if confidence < min_confidence:
        errors.append(
            f"Confidence score {confidence} is below the minimum threshold {min_confidence}"
        )

    if document_type == "invoice":
        invoice = InvoiceFields(**extracted_data)
        if not invoice.vendor:
            errors.append("Vendor name is missing")
        if not invoice.date:
            errors.append("Invoice date is missing")
        if invoice.total is None:
            errors.append("Total amount is missing")
        if not invoice.line_items:
            errors.append("Line items are missing")

    elif document_type == "receipt":
        receipt = ReceiptFields(**extracted_data)
        if not receipt.merchant:
            errors.append("Merchant name is missing")
        if receipt.total is None:
            errors.append("Total amount is missing")
        if not receipt.items:
            errors.append("Items are missing")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "confidence": confidence,
    }
