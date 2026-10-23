from typing import Dict, List, Optional, TypedDict, Any
from datetime import datetime


class LineItem(TypedDict):
    description: str
    quantity: float
    unit_price: float
    amount: float


class InvoiceFields(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]
    confidence: float


class ReceiptItem(TypedDict):
    name: str
    price: float
    quantity: Optional[float]


class ReceiptFields(TypedDict):
    merchant: str
    tax: float
    total: float
    items: List[ReceiptItem]
    confidence: float


class NormalizedLineItem(TypedDict):
    description: str
    quantity: float
    unit_price: float
    amount: float
    category: str


class NormalizedExpense(TypedDict):
    vendor: str
    merchant: str
    date: str
    total: float
    tax: float
    currency: str
    line_items: List[NormalizedLineItem]
    items: List[Dict[str, Any]]
    document_type: str
    confidence: float


class ValidationResult(TypedDict):
    is_valid: bool
    missing_fields: List[str]
    confidence: float
    errors: List[str]


def parse_date(date_str: str) -> Optional[str]:
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None


def format_currency(amount: float) -> str:
    return f"${amount:.2f}"
