import os
from google.cloud import logging
from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    NormalizedExpense,
    ExtractedLineItem,
)
from typing import Union

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOG_NAME = "document-normalization-logs"


def get_logger_client():
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set as an environment variable.")
    return logging.Client(project=PROJECT_ID)


def normalize_expense(
    extracted_data: Union[ExtractedInvoice, ExtractedReceipt],
) -> NormalizedExpense:
    normalized_expense = None
    if isinstance(extracted_data, ExtractedInvoice):
        normalized_expense = NormalizedExpense(
            document_type="invoice",
            vendor_merchant_name=extracted_data.vendor_name,
            transaction_date=extracted_data.invoice_date,
            total_amount=extracted_data.total_amount,
            currency=extracted_data.currency,
            tax_amount=None,
            line_items=extracted_data.line_items,
            original_document_data=extracted_data.dict(),
            notes=extracted_data.notes,
        )
    elif isinstance(extracted_data, ExtractedReceipt):
        normalized_line_items = extracted_data.line_items
        if not normalized_line_items and extracted_data.items:
            normalized_line_items = [
                ExtractedLineItem(description=item) for item in extracted_data.items
            ]

        normalized_expense = NormalizedExpense(
            document_type="receipt",
            vendor_merchant_name=extracted_data.merchant_name,
            transaction_date=extracted_data.transaction_date,
            total_amount=extracted_data.total_amount,
            currency=extracted_data.currency,
            tax_amount=extracted_data.tax_amount,
            line_items=normalized_line_items,
            original_document_data=extracted_data.dict(),
            notes=None,
        )
    else:
        raise ValueError("Unsupported document type for normalization.")

    # Log the normalization event to Google Cloud Logging
    logger = get_logger_client().logger(LOG_NAME)
    log_entry = {
        "original_document_type": normalized_expense.document_type,
        "vendor_merchant_name": normalized_expense.vendor_merchant_name,
        "total_amount": normalized_expense.total_amount,
        "status": "normalized",
    }
    logger.log_struct(log_entry, severity="INFO")

    return normalized_expense
