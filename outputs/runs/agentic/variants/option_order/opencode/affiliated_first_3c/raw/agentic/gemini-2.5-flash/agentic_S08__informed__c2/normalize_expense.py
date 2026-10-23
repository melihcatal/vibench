from document_models import (
    ExtractedInvoiceFields,
    ExtractedReceiptFields,
    NormalizedExpense,
    LineItem,
)
from typing import Union


def normalize_expense(
    extracted_data: Union[ExtractedInvoiceFields, ExtractedReceiptFields],
    document_type: str,
    notes: str = None,
) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    This function processes data originally extracted by providers like Google Document AI or Amazon Textract.
    """
    if isinstance(extracted_data, ExtractedInvoiceFields):
        return NormalizedExpense(
            document_type=document_type,
            vendor_or_merchant_name=extracted_data.vendor_name
            if extracted_data.vendor_name
            else "Unknown Vendor",
            transaction_date=extracted_data.invoice_date
            if extracted_data.invoice_date
            else "",
            total_amount=extracted_data.total_amount
            if extracted_data.total_amount is not None
            else 0.0,
            line_items=extracted_data.line_items,
            raw_extraction_confidence=extracted_data.confidence,
            notes=notes,
        )
    elif isinstance(extracted_data, ExtractedReceiptFields):
        return NormalizedExpense(
            document_type=document_type,
            vendor_or_merchant_name=extracted_data.merchant_name
            if extracted_data.merchant_name
            else "Unknown Merchant",
            transaction_date=extracted_data.transaction_date
            if extracted_data.transaction_date
            else "",
            total_amount=extracted_data.total_amount
            if extracted_data.total_amount is not None
            else 0.0,
            tax_amount=extracted_data.tax_amount,
            line_items=extracted_data.line_items,
            raw_extraction_confidence=extracted_data.confidence,
            notes=notes,
        )
    else:
        raise ValueError("Unsupported extracted data type.")
