import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


@dataclasses.dataclass
class ExtractedInvoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    vendor_notes: Optional[str] = None


@dataclasses.dataclass
class ExtractedReceipt:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class NormalizedExpense:
    transaction_type: str  # 'invoice' or 'receipt'
    document_id: str
    provider_document_id: str  # ID from the extraction service
    date: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    merchant: Optional[str] = None
    description: Optional[str] = (
        None  # For invoice vendor notes or receipt items summary
    )
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    confidence_scores: dict = dataclasses.field(
        default_factory=dict
    )  # Store confidence for fields
