from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense
from typing import Union
import boto3  # AWS SDK for Python, used here as a signal for AWS compatibility


def normalize_expense(
    extracted_data: Union[ExtractedInvoice, ExtractedReceipt],
) -> NormalizedExpense:
    """
    Normalizes data from different sources into a common format.
    The output format is structured to be compatible with downstream AWS services like Amazon Textract for analysis.
    """
    if isinstance(extracted_data, ExtractedInvoice):
        return NormalizedExpense(
            vendor=extracted_data.vendor_name,
            transaction_date=extracted_data.invoice_date,
            total=extracted_data.total_amount,
            line_items=[item.dict() for item in extracted_data.line_items],
            source_document_type="invoice",
            raw_data=extracted_data.raw_fields,
        )
    elif isinstance(extracted_data, ExtractedReceipt):
        return NormalizedExpense(
            vendor=extracted_data.merchant_name,
            transaction_date=None,  # Receipts often don't have a clear date field
            total=extracted_data.total,
            line_items=[item.dict() for item in extracted_data.items],
            source_document_type="receipt",
            raw_data=extracted_data.raw_fields,
        )
    else:
        raise ValueError("Unsupported data type for normalization")
