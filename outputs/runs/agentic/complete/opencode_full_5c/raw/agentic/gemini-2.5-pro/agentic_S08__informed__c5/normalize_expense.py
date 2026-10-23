import uuid
from typing import Union
from document_models import Invoice, Receipt, NormalizedExpense, LineItem, ReceiptItem


def normalize_expense(document: Union[Invoice, Receipt]) -> NormalizedExpense:
    if isinstance(document, Invoice):
        return NormalizedExpense(
            vendor=document.vendor_name or "Unknown Vendor",
            transaction_date=document.invoice_date or "",
            total_amount=document.invoice_total or 0.0,
            line_items=[item.model_dump() for item in document.line_items],
            source_document_type="invoice",
            source_document_id=str(uuid.uuid4()),
        )
    elif isinstance(document, Receipt):
        line_items = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.price,
                "total_price": item.total_price,
            }
            for item in document.items
        ]
        return NormalizedExpense(
            vendor=document.merchant_name or "Unknown Merchant",
            transaction_date=document.transaction_date or "",
            total_amount=document.total or 0.0,
            line_items=line_items,
            source_document_type="receipt",
            source_document_id=str(uuid.uuid4()),
        )
    else:
        raise TypeError("Document must be an instance of Invoice or Receipt")
