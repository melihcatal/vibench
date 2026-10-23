from document_models import Invoice, Receipt, NormalizedExpense, LineItem
from typing import Union

def normalize_expense(document: Union[Invoice, Receipt], document_type: str, provider: str = "google_document_ai") -> NormalizedExpense:
    if isinstance(document, Invoice):
        return NormalizedExpense(
            document_type=document_type,
            provider=provider,
            vendor_name=document.vendor_name,
            transaction_date=document.invoice_date,
            total_amount=document.total_amount,
            currency="USD", # Assuming USD for now, can be extracted from document if available
            line_items=document.line_items,
            raw_extraction=document.__dict__ # Store raw data for debugging/auditing
        )
    elif isinstance(document, Receipt):
        return NormalizedExpense(
            document_type=document_type,
            provider=provider,
            vendor_name=document.merchant_name,
            transaction_date=document.transaction_date,
            total_amount=document.total_amount,
            currency="USD", # Assuming USD for now
            line_items=document.items,
            raw_extraction=document.__dict__
        )
    else:
        raise ValueError("Unsupported document type for normalization.")
