# [HELPER] document_models.py
# Define local request, response, and normalization helpers for Structured Document Extraction

from typing import TypedDict, List

# Request model for sending documents to an extraction service


class ExtractionRequest(TypedDict):
    content: bytes  # Raw bytes of PDF or image
    mime_type: str  # e.g. 'application/pdf' or 'image/png'
    options: dict | None = None  # Provider-specific options


# Shared response structure after extraction (prior to normalization)
class ExtractionResponse(TypedDict):
    vendor: str | None
    merchant: str | None
    date: str | None
    total: str | None
    line_items: List[str] | None
    items: List[str] | None
    tax: str | None
    confidence: float | None


# Normalized expense schema used downstream


class NormalizedExpense(TypedDict):
    vendor: str
    merchant: str
    date: str
    total: float
    tax: float
    items: List[str]
    confidence: float


# Helper to cast raw strings to numeric types safely
def safe_float(val: str | None) -> float:
    try:
        return float(val or 0)
    except ValueError:
        return 0.0
