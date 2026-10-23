from document_models import InvoiceFields, ReceiptFields, NormalizedExpense, LineItem
from typing import Union, Dict, Any


def normalize_expense(
    extracted_data: Union[InvoiceFields, ReceiptFields],
    document_type: str,
    raw_extraction: Dict[str, Any],
) -> NormalizedExpense:
    if document_type == "invoice":
        if not isinstance(extracted_data, InvoiceFields):
            raise ValueError("Expected InvoiceFields for document_type 'invoice'")
        return NormalizedExpense(
            document_type="invoice",
            vendor_name=extracted_data.vendor_name,
            transaction_date=extracted_data.invoice_date,
            total_amount=extracted_data.invoice_total,
            tax_amount=None,  # Invoices don't always have a dedicated tax field, might be part of line items
            currency=None,  # Document Intelligence prebuilt invoice doesn't explicitly provide currency at top level
            line_items=extracted_data.line_items,
            raw_extraction=raw_extraction,
        )
    elif document_type == "receipt":
        if not isinstance(extracted_data, ReceiptFields):
            raise ValueError("Expected ReceiptFields for document_type 'receipt'")
        return NormalizedExpense(
            document_type="receipt",
            vendor_name=extracted_data.merchant_name,
            transaction_date=extracted_data.transaction_date,
            total_amount=extracted_data.total_amount,
            tax_amount=extracted_data.tax_amount,
            currency=None,  # Document Intelligence prebuilt receipt doesn't explicitly provide currency at top level
            line_items=extracted_data.line_items,
            raw_extraction=raw_extraction,
        )
    else:
        raise ValueError(f"Unknown document type: {document_type}")
