from typing import Union
from document_models import Invoice, Receipt, NormalizedExpense


def normalize_to_expense(document: Union[Invoice, Receipt]) -> NormalizedExpense:
    if isinstance(document, Invoice):
        return NormalizedExpense(
            vendor=document.vendor_name or "Unknown Vendor",
            transaction_date=document.invoice_date or "",
            total=document.total,
            currency=document.currency or "USD",
            items=document.line_items,
            source_document_type="invoice",
            source_document_id=document.invoice_id,
        )
    elif isinstance(document, Receipt):
        return NormalizedExpense(
            vendor=document.merchant_name or "Unknown Merchant",
            transaction_date=document.transaction_date or "",
            total=document.total,
            currency=document.currency or "USD",
            items=document.line_items,
            source_document_type="receipt",
        )
    else:
        raise TypeError("Document must be of type Invoice or Receipt")
