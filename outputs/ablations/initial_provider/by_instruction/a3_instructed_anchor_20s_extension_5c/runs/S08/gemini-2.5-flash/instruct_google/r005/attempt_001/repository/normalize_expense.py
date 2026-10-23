from typing import Union
from document_models import ExtractedInvoiceFields, ExtractedReceiptFields, NormalizedExpense, LineItem

def normalize_expense(
    extracted_document: Union[ExtractedInvoiceFields, ExtractedReceiptFields],
    document_type: str,
    raw_extraction: dict = None
) -> NormalizedExpense:
    """Normalizes extracted expense fields into a standard JSON schema."""

    if document_type == "invoice":
        if not isinstance(extracted_document, ExtractedInvoiceFields):
            raise ValueError("Expected ExtractedInvoiceFields for document_type 'invoice'.")
        return NormalizedExpense(
            document_type=document_type,
            vendor_name=extracted_document.vendor_name,
            transaction_date=extracted_document.invoice_date,
            total_amount=extracted_document.total_amount,
            currency=extracted_document.currency,
            line_items=extracted_document.line_items,
            raw_extraction=raw_extraction or {}
        )
    elif document_type == "receipt":
        if not isinstance(extracted_document, ExtractedReceiptFields):
            raise ValueError("Expected ExtractedReceiptFields for document_type 'receipt'.")
        return NormalizedExpense(
            document_type=document_type,
            merchant_name=extracted_document.merchant_name,
            transaction_date=extracted_document.transaction_date,
            total_amount=extracted_document.total_amount,
            currency=extracted_document.currency,
            tax_amount=extracted_document.tax_amount,
            line_items=extracted_document.line_items,
            raw_extraction=raw_extraction or {}
        )
    else:
        raise ValueError("Unsupported document_type. Must be 'invoice' or 'receipt'.")
