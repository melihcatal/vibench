from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class LineItem(BaseModel):
    description: str
    amount: float
    quantity: float = 1.0


class ExtractedInvoiceData(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]
    confidence: float
    provider: str


class ExtractedReceiptData(BaseModel):
    merchant: str
    tax: float
    total: float
    items: List[LineItem]
    confidence: float
    provider: str


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: str
    total_amount: float
    tax_amount: float
    line_items: List[LineItem]
    metadata: Dict[str, Any]


class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str]
    low_confidence_fields: List[str]
    confidence_score: float


def parse_date(date_str: str) -> str:
    """
    Parse and normalize date strings into ISO format.
    """
    try:
        if len(date_str.split("-")) == 3:
            return date_str
        elif len(date_str.split("/")) == 3:
            month, day, year = date_str.split("/")
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        elif len(date_str.split(".")) == 3:
            day, month, year = date_str.split(".")
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            return date_str
    except:
        return date_str
