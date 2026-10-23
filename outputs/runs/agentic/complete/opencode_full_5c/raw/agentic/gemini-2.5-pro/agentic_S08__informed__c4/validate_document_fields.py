from document_models import Invoice, Receipt, ValidationResult
from typing import Union


def validate_extracted_fields(document: Union[Invoice, Receipt]) -> ValidationResult:
    errors = []

    if isinstance(document, Invoice):
        if not document.vendor_name:
            errors.append("Vendor name is missing.")
        if not document.invoice_date:
            errors.append("Invoice date is missing.")
        if document.invoice_total is None:
            errors.append("Invoice total is missing.")

        if (
            "VendorName" in document.raw_fields
            and document.raw_fields["VendorName"].get("confidence", 1.0) < 0.8
        ):
            errors.append("Vendor name confidence is low.")

    elif isinstance(document, Receipt):
        if not document.merchant_name:
            errors.append("Merchant name is missing.")
        if not document.transaction_date:
            errors.append("Transaction date is missing.")
        if document.total is None:
            errors.append("Total amount is missing.")

        if (
            "MerchantName" in document.raw_fields
            and document.raw_fields["MerchantName"].get("confidence", 1.0) < 0.8
        ):
            errors.append("Merchant name confidence is low.")

    return ValidationResult(is_valid=not errors, errors=errors)
