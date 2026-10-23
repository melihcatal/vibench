from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class FieldConfidence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ExtractedField:
    name: str
    value: Any
    confidence: float
    raw_text: Optional[str] = None
    bounding_box: Optional[List[Dict[str, float]]] = None


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    total_price: float
    confidence: float


@dataclass
class InvoiceExtraction:
    vendor_name: ExtractedField
    invoice_date: ExtractedField
    invoice_total: ExtractedField
    line_items: List[LineItem]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReceiptExtraction:
    merchant_name: ExtractedField
    transaction_date: ExtractedField
    tax_amount: ExtractedField
    total_amount: ExtractedField
    items: List[LineItem]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpense:
    expense_id: str
    vendor: str
    date: datetime
    total_amount: float
    currency: str
    line_items: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0


@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: List[str]
    low_confidence_fields: List[str]
    overall_confidence: float
    validation_errors: List[str] = field(default_factory=list)


def normalize_azure_field(field_dict: Dict[str, Any]) -> ExtractedField:
    value = field_dict.get("value")
    confidence = field_dict.get("confidence", 0.0)
    content = field_dict.get("content", "")

    return ExtractedField(
        name=field_dict.get("key", {}).get("content", ""),
        value=value,
        confidence=confidence,
        raw_text=content,
    )


def parse_azure_line_items(fields: List[Dict[str, Any]]) -> List[LineItem]:
    line_items = []
    for field in fields:
        if "description" in field.get("key", {}).get("content", "").lower():
            desc = field.get("value", {}).get("content", "")
            qty = float(field.get("quantity", {}).get("content", "1"))
            unit_price = float(field.get("unitPrice", {}).get("content", "0"))
            total = float(field.get("totalPrice", {}).get("content", "0"))
            conf = field.get("confidence", 0.0)

            line_items.append(
                LineItem(
                    description=desc,
                    quantity=qty,
                    unit_price=unit_price,
                    total_price=total,
                    confidence=conf,
                )
            )
    return line_items


def create_expense_id(vendor: str, date: datetime, total: float) -> str:
    vendor_slug = vendor.lower().replace(" ", "_")[:20]
    date_str = date.strftime("%Y%m%d")
    total_hash = hash(str(total)) % 10000
    return f"exp_{vendor_slug}_{date_str}_{total_hash:04d}"
