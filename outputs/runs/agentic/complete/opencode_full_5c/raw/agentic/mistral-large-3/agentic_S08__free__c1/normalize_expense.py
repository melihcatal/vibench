from typing import Dict, Any
from document_models import (
    NormalizedExpense,
    InvoiceFields,
    ReceiptFields,
    normalize_currency,
)


def normalize_expense(
    extracted_data: Dict[str, Any], document_type: str
) -> Dict[str, Any]:
    if document_type == "invoice":
        invoice = InvoiceFields(**extracted_data)
        normalized = NormalizedExpense(
            vendor_merchant=invoice.vendor,
            date=invoice.date,
            amount=normalize_currency(invoice.total),
            tax=None,
            line_items=invoice.line_items,
            metadata={
                "document_type": document_type,
                "original_confidence": invoice.confidence,
            },
        )
    elif document_type == "receipt":
        receipt = ReceiptFields(**extracted_data)
        normalized = NormalizedExpense(
            vendor_merchant=receipt.merchant,
            date=None,
            amount=normalize_currency(receipt.total),
            tax=normalize_currency(receipt.tax),
            line_items=[],
            metadata={
                "document_type": document_type,
                "original_confidence": receipt.confidence,
                "items": receipt.items,
            },
        )
    else:
        raise ValueError(f"Unsupported document type: {document_type}")

    return normalized.dict()
