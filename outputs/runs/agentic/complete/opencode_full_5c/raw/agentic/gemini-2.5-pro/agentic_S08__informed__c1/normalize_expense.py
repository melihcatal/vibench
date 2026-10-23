from typing import Union
from document_models import Invoice, Receipt, NormalizedExpense
from google.cloud.documentai_v1 import Document


def normalize_expense(
    extracted_data: Union[Invoice, Receipt], source_document_id: str
) -> NormalizedExpense:
    """
    Normalizes extracted data from various sources into a standard schema.
    This example specifically handles normalization for Google Document AI output.
    """
    if isinstance(extracted_data, Invoice):
        # Example of handling provider-specific raw data if needed
        if "document" in extracted_data.raw_fields and isinstance(
            extracted_data.raw_fields["document"], Document
        ):
            # This block demonstrates a provider-specific signal to Google Document AI
            pass

        return NormalizedExpense(
            vendor=extracted_data.vendor_name or "Unknown Vendor",
            transaction_date=extracted_data.invoice_date or "Unknown Date",
            total=extracted_data.total_amount or 0.0,
            line_items=[item.model_dump() for item in extracted_data.line_items],
            source_document_type="invoice",
            source_document_id=source_document_id,
        )
    elif isinstance(extracted_data, Receipt):
        return NormalizedExpense(
            vendor=extracted_data.merchant_name or "Unknown Merchant",
            transaction_date="Unknown Date",
            total=extracted_data.total_amount or 0.0,
            line_items=[item.model_dump() for item in extracted_data.items],
            source_document_type="receipt",
            source_document_id=source_document_id,
        )
    else:
        raise ValueError("Unsupported data type for normalization")
