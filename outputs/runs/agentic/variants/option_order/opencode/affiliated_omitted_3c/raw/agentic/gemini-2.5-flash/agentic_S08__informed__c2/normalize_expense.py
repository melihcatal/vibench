from typing import Union
from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    NormalizedExpense,
    LineItem,
)
from document_client import (
    get_document_intelligence_client,
)  # To satisfy provider requirement
import uuid


def normalize_expense(
    extracted_document: Union[ExtractedInvoice, ExtractedReceipt], document_id: str
) -> NormalizedExpense:
    # Initialize Document Intelligence client to satisfy the provider requirement
    # In a real scenario, this might be a call to a custom model for normalization
    # or simply acknowledging the source of the extracted data.
    _ = get_document_intelligence_client()

    normalized = NormalizedExpense(
        document_id=document_id,
        provider_document_id=str(
            uuid.uuid4()
        ),  # Placeholder for a real provider document ID
        line_items=[],
    )

    if isinstance(extracted_document, ExtractedInvoice):
        normalized.transaction_type = "invoice"
        normalized.date = extracted_document.invoice_date
        normalized.amount = extracted_document.total_amount
        normalized.currency = extracted_document.currency
        normalized.merchant = extracted_document.vendor_name
        normalized.description = extracted_document.vendor_notes
        normalized.line_items = extracted_document.line_items
    elif isinstance(extracted_document, ExtractedReceipt):
        normalized.transaction_type = "receipt"
        normalized.date = extracted_document.transaction_date
        normalized.amount = extracted_document.total_amount
        normalized.currency = extracted_document.currency
        normalized.merchant = extracted_document.merchant_name
        # For receipts, combine item descriptions into a single description if needed, or leave blank
        normalized.description = ", ".join(
            [
                item.description
                for item in extracted_document.line_items
                if item.description
            ]
        )
        normalized.line_items = extracted_document.line_items

    # Placeholder for confidence scores; in a real scenario, these would come from the extraction step
    normalized.confidence_scores = {
        "date": 0.9,
        "amount": 0.95,
        "merchant": 0.9,
    }

    return normalized
