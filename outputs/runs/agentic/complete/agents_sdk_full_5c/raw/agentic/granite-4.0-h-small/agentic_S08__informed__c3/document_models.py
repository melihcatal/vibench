from dataclasses import dataclass, field
from typing import List, Optional, Union

@dataclass
class Amount:
    value: float = 0.0
    currency: str = "USD"

@dataclass
class LineItem:
    description: str = ""
    quantity: int = 1
    unit_price: Amount = field(default_factory=Amount)
    total: Amount = field(default_factory=Amount)
    tax: Amount = field(default_factory=Amount)

@dataclass
class ExpenseRecord:
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[Amount] = None
    line_items: List[LineItem] = field(default_factory=list)
    # Raw extraction payload (e.g., raw JSON from Mindee, Textract, etc.)
    raw_data: dict = field(default_factory=dict)
    confidence: dict = field(default_factory=dict)

@dataclass
class NormalizedExpense:
    vendor: str = "UNKNOWN_VENDOR"
    date: str = ""
    total: float = 0.0
    currency: str = "USD"
    line_items: List[Dict] = field(default_factory=list)

@dataclass
class InvoiceExtractionRequest:
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)

@dataclass
class ReceiptExtractionRequest:
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)

@dataclass
class InvoiceExtractionResponse:
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)

@dataclass
class ReceiptExtractionResponse:
    merchant: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
