# [HELPER] document_models.py
# Local request, response, and normalization helpers for Structured Document Extraction

from typing import TypedDict, List, Optional
from datetime import datetime


class InvoiceExtractionResult(TypedDict):
    vendor: Optional[str]
    date: Optional[datetime]
    total: Optional[float]
    line_items: Optional[List[dict]]


class ReceiptExtractionResult(TypedDict):
    merchant: Optional[str]
    tax: Optional[float]
    total: Optional[float]
    items: Optional[List[dict]]


class NormalizedExpense(TypedDict):
    vendor: Optional[str]
    date: Optional[str]  # ISO string
    total: Optional[float]
    line_items: Optional[List[dict]]


class ValidationIssue(TypedDict):
    field: str
    reason: str


# Helper utility functions


def _parse_date(date_str: str) -> Optional[str]:
    """Parse various date formats into ISO 8601 string."""
    try:
        from dateutil import parser as dparser

        return dparser.parse(date_str).date().isoformat()
    except Exception:
        return None
