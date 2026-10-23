# [SAME-SCENARIO] normalize_expense.py
# Normalizes extracted expense fields into a standard JSON schema

import json
from document_models import NormalizedExpense


def normalize_expense(extraction_result):
    """Transform provider-specific extraction result into a unified schema.

    Args:
        extraction_result (Union[InvoiceExtractionResult, ReceiptExtractionResult]): Raw extraction output.

    Returns:
        NormalizedExpense: Standardized JSON-ready dict.
    """
    # Example implementation for invoice; add receipt logic similarly
    if hasattr(extraction_result, "vendor") and hasattr(extraction_result, "total"):
        return {
            "vendor": extraction_result.vendor,
            "date": extraction_result.date,
            "total": extraction_result.total,
            "line_items": extraction_result.line_items,
        }
    else:
        raise ValueError("Unsupported extraction type")
