from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ExtractedField:
    value: Any
    confidence: float
    field_name: str
    page_number: Optional[int] = None
    bounding_box: Optional[List[float]] = None # [x1, y1, x2, y2]

@dataclass
class LineItem:
    description: Optional[ExtractedField] = None
    quantity: Optional[ExtractedField] = None
    unit_price: Optional[ExtractedField] = None
    total_price: Optional[ExtractedField] = None

@dataclass
class DocumentExtractionResponse:
    vendor_name: Optional[ExtractedField] = None
    invoice_date: Optional[ExtractedField] = None
    total_amount: Optional[ExtractedField] = None
    currency: Optional[ExtractedField] = None
    line_items: List[LineItem] = field(default_factory=list)
    document_type: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

@dataclass
class NormalizedExpense:
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    document_type: Optional[str] = None

def normalize_document_extraction_response(response: DocumentExtractionResponse) -> NormalizedExpense:
    """
    Normalizes the extracted document fields into a standard JSON schema.
    """
    normalized_line_items = []
    for item in response.line_items:
        normalized_item = {}
        if item.description and item.description.value is not None:
            normalized_item["description"] = item.description.value
        if item.quantity and item.quantity.value is not None:
            normalized_item["quantity"] = item.quantity.value
        if item.unit_price and item.unit_price.value is not None:
            normalized_item["unit_price"] = item.unit_price.value
        if item.total_price and item.total_price.value is not None:
            normalized_item["total_price"] = item.total_price.value
        if normalized_item:
            normalized_line_items.append(normalized_item)

    return NormalizedExpense(
        vendor_name=response.vendor_name.value if response.vendor_name else None,
        transaction_date=response.invoice_date.value if response.invoice_date else None,
        total_amount=response.total_amount.value if response.total_amount else None,
        currency=response.currency.value if response.currency else None,
        line_items=normalized_line_items,
        document_type=response.document_type
    )
