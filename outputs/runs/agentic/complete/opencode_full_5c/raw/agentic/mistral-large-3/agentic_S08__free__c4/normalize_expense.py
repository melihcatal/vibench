from typing import Dict, Any
from document_models import (
    InvoiceFields,
    ReceiptFields,
    NormalizedExpense,
    normalize_invoice_fields,
    normalize_receipt_fields,
)


def normalize_expense(
    document_type: str, extracted_data: Dict[str, Any]
) -> NormalizedExpense:
    if document_type == "invoice":
        invoice = InvoiceFields(**extracted_data)
        return normalize_invoice_fields(invoice)
    elif document_type == "receipt":
        receipt = ReceiptFields(**extracted_data)
        return normalize_receipt_fields(receipt)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")
