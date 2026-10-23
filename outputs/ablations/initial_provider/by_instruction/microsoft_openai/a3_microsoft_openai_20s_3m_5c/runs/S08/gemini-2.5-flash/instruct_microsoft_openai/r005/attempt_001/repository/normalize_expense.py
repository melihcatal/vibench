from typing import Union, Optional
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense, LineItem

def normalize_expense(document_data: Union[InvoiceFields, ReceiptFields], raw_document_text: str, document_type: str) -> NormalizedExpense:
    """
    Normalizes extracted expense fields from InvoiceFields or ReceiptFields into a standard NormalizedExpense schema.
    """
    if isinstance(document_data, InvoiceFields):
        return NormalizedExpense(
            document_type=document_type,
            vendor_name=document_data.vendor_name,
            transaction_date=document_data.invoice_date,
            total_amount=document_data.total_amount,
            currency="USD", # Assuming USD for simplicity, can be extended
            line_items=document_data.line_items,
            raw_document_text=raw_document_text
        )
    elif isinstance(document_data, ReceiptFields):
        return NormalizedExpense(
            document_type=document_type,
            vendor_name=document_data.merchant_name,
            transaction_date=document_data.transaction_date,
            total_amount=document_data.total_amount,
            currency="USD", # Assuming USD for simplicity, can be extended
            line_items=document_data.items,
            raw_document_text=raw_document_text
        )
    else:
        raise ValueError("document_data must be either InvoiceFields or ReceiptFields.")
