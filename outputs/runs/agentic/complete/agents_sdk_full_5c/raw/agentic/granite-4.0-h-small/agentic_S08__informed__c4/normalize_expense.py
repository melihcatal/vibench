# [SAME-SCENARIO] normalize_expense.py
from document_models import ExtractionBase, NormalizedExpense
import typing as t

def normalize_expense(extracted: ExtractionBase) -> NormalizedExpense:
    """Convert generic extraction result (invoice or receipt) to a standard JSON schema.

    Args:
        extracted: An instance of InvoiceExtractionResponse or ReceiptExtractionResponse.
    Returns:
        NormalizedExpense containing common fields.
    """
    # Determine the source type via subclass check
    if isinstance(extracted, InvoiceExtractionResponse):
        vendor_name = extracted.vendor
        date = extracted.date
        total = extracted.total
        items = [] if not hasattr(extracted, 'line_items') else extracted.line_items
    elif isinstance(extracted, ReceiptExtractionResponse):
        vendor_name = extracted.merchant
        date = None  # receipts often lack a clear date field
        total = extracted.total
        items = [] if not hasattr(extracted, 'items') else extracted.items
    else:
        raise TypeError('Unsupported extraction type')
    return NormalizedExpense(
        vendor=vendor_name,
        date=date,
        amount=total,
        line_items=items,
        source_type='invoice' if isinstance(extracted, InvoiceExtractionResponse) else 'receipt'
    )