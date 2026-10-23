# Request, Response, and Normalization helpers for Structured Document Extraction

import json
from typing import TypedDict, List, Optional

# ---------------------------------------------------------------------------
# Core data models
# ---------------------------------------------------------------------------


class Item(TypedDict):
    description: str
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None


class ExpenseRecord(TypedDict):
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    items: Optional[List[Item]] = None
    line_items: Optional[List[Item]] = None
    tax: Optional[float] = None
    confidence: float = 1.0


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------


def merge_invoice_receipt(source: dict) -> ExpenseRecord:
    """
    Convert raw extraction results from invoice or receipt providers into the
    standard ExpenseRecord schema.  Handles different key names (vendor vs
    merchant, line_items vs items) and injects confidence metadata.
    """
    record: ExpenseRecord = {
        "vendor": source.get("vendor") or source.get("merchant"),
        "date": source.get("date"),
        "total": source.get("total"),
        "items": source.get("line_items") or source.get("items"),
        "tax": source.get("tax"),
        "confidence": source.get("confidence", 1.0),
    }
    # Normalize fields: ensure required keys exist, use None if missing
    record["items"] = record["items"] if record["items"] is not None else []
    return record


# ---------------------------------------------------------------------------
# Validation utilities (optional but useful for later steps)
# ---------------------------------------------------------------------------


def validate(expense: ExpenseRecord) -> bool:
    """
    Simple validation: required fields must be present and confidence >= 0.7.
    Adjust as needed for stricter business rules.
    """
    required = ["vendor", "date", "total"]
    for field in required:
        if not expense.get(field):
            return False
    return expense["confidence"] >= 0.7
