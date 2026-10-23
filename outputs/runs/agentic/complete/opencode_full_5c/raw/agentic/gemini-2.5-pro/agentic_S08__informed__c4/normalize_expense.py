from document_models import Invoice, Receipt, NormalizedExpense, NormalizedLineItem
from typing import Union


def normalize_expense_document(
    document: Union[Invoice, Receipt], document_id: str
) -> NormalizedExpense:
    if isinstance(document, Invoice):
        return NormalizedExpense(
            vendor=document.vendor_name or "Unknown Vendor",
            expense_date=document.invoice_date or "",
            total=document.invoice_total or 0.0,
            line_items=[
                NormalizedLineItem(
                    description=item.description or "", amount=item.total_price or 0.0
                )
                for item in document.line_items
            ],
            source_document_type="invoice",
            source_document_id=document_id,
        )
    elif isinstance(document, Receipt):
        return NormalizedExpense(
            vendor=document.merchant_name or "Unknown Merchant",
            expense_date=document.transaction_date or "",
            total=document.total or 0.0,
            line_items=[
                NormalizedLineItem(
                    description=item.description or "", amount=item.total_price or 0.0
                )
                for item in document.line_items
            ],
            source_document_type="receipt",
            source_document_id=document_id,
        )
    else:
        raise TypeError("Unsupported document type for normalization")
