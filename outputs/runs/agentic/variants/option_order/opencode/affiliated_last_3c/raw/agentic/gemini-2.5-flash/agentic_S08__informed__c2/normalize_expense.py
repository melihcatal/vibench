from typing import Union
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense


def normalize_expense(
    extracted_document: Union[ExtractedInvoice, ExtractedReceipt],
) -> NormalizedExpense:
    if isinstance(extracted_document, ExtractedInvoice):
        return NormalizedExpense(
            document_type="invoice",
            vendor_name=extracted_document.vendor_name.value,
            transaction_date=extracted_document.invoice_date.value,
            total_amount=extracted_document.total_amount.value,
            currency=extracted_document.currency.value,
            tax_amount=None,  # Invoices might not always have an explicit tax field extracted
            line_items=extracted_document.line_items,
            notes=extracted_document.notes.value if extracted_document.notes else None,
            raw_extraction=extracted_document.model_dump(),
        )
    elif isinstance(extracted_document, ExtractedReceipt):
        return NormalizedExpense(
            document_type="receipt",
            vendor_name=extracted_document.merchant_name.value,
            transaction_date=extracted_document.receipt_date.value,
            total_amount=extracted_document.total_amount.value,
            currency=extracted_document.currency.value,
            tax_amount=extracted_document.tax_amount.value,
            line_items=extracted_document.line_items,
            notes=None,  # Receipts typically don't have a 'notes' field
            raw_extraction=extracted_document.model_dump(),
        )
    else:
        raise ValueError("Unsupported document type for normalization")
