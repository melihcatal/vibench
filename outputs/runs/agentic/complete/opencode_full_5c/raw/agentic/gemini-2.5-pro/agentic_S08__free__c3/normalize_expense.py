from typing import Union
from document_models import Invoice, Receipt, NormalizedExpense, LineItem, ReceiptItem


def normalize_expense(document: Union[Invoice, Receipt]) -> NormalizedExpense:
    """
    Normalizes fields from an Invoice or Receipt into a standard expense schema.
    """
    if isinstance(document, Invoice):
        return NormalizedExpense(
            vendor=document.vendor_name or "Unknown Vendor",
            transaction_date=document.invoice_date or "Unknown Date",
            total=document.total_amount or 0.0,
            line_items=[item.dict() for item in document.line_items],
            source_document_type="invoice",
        )
    elif isinstance(document, Receipt):
        return NormalizedExpense(
            vendor=document.merchant_name or "Unknown Merchant",
            transaction_date="Unknown Date",  # Receipts in this model don't have a date
            total=document.total or 0.0,
            line_items=[item.dict() for item in document.items],
            source_document_type="receipt",
        )
    else:
        raise TypeError("Unsupported document type for normalization.")
