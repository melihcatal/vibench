from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class FieldConfidence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class LineItem:
    """Model for line item data."""

    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "confidence": self.confidence,
        }


@dataclass
class ExtractedDocument:
    """Base model for extracted document data."""

    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    confidence_scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "vendor": self.vendor,
            "merchant": self.merchant,
            "date": self.date,
            "total": self.total,
            "tax": self.tax,
            "currency": self.currency,
            "line_items": [item.to_dict() for item in self.line_items],
            "confidence_scores": self.confidence_scores,
            "extracted_at": datetime.utcnow().isoformat(),
        }


@dataclass
class NormalizedExpense:
    """Model for normalized expense data."""

    id: Optional[str] = None
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: float = 0.0
    tax_amount: Optional[float] = None
    currency: str = "USD"
    category: Optional[str] = None
    description: Optional[str] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    normalized_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @classmethod
    def from_extracted(cls, extracted: ExtractedDocument) -> "NormalizedExpense":
        """Create normalized expense from extracted document."""
        vendor = extracted.vendor or extracted.merchant

        line_items = []
        for item in extracted.line_items:
            line_items.append(
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "amount": item.amount
                    or (
                        item.quantity * item.unit_price
                        if item.quantity and item.unit_price
                        else None
                    ),
                }
            )

        return cls(
            vendor_name=vendor,
            merchant_name=extracted.merchant,
            transaction_date=extracted.date,
            total_amount=extracted.total or 0.0,
            tax_amount=extracted.tax,
            currency=extracted.currency,
            line_items=line_items,
            metadata={
                "document_type": extracted.document_type,
                "confidence_scores": extracted.confidence_scores,
                "raw_data": extracted.raw_data,
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "vendor_name": self.vendor_name,
            "merchant_name": self.merchant_name,
            "transaction_date": self.transaction_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "category": self.category,
            "description": self.description,
            "line_items": self.line_items,
            "metadata": self.metadata,
            "normalized_at": self.normalized_at,
        }

        if self.id:
            result["id"] = self.id

        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class ValidationResult:
    """Model for validation results."""

    def __init__(
        self, is_valid: bool, errors: List[str], confidence_scores: Dict[str, float]
    ):
        self.is_valid = is_valid
        self.errors = errors
        self.confidence_scores = confidence_scores

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "confidence_scores": self.confidence_scores,
            "overall_confidence": self.confidence_scores.get("overall", 0.0),
        }

    @property
    def overall_confidence(self) -> float:
        return self.confidence_scores.get("overall", 0.0)


def create_extraction_request(
    file_path: str, document_type: str, options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a standardized extraction request."""
    return {
        "file_path": file_path,
        "document_type": document_type,
        "options": options or {},
        "requested_at": datetime.utcnow().isoformat(),
    }


def parse_extraction_response(
    response_data: Dict[str, Any], provider: str
) -> ExtractedDocument:
    """Parse provider response into standardized extracted document."""
    document_type = response_data.get("document_type", "unknown")

    extracted = ExtractedDocument(document_type=document_type)

    field_mappings = {
        "vendor": ["vendor", "VendorName", "vendor_name"],
        "merchant": ["merchant", "MerchantName", "merchant_name"],
        "date": ["date", "InvoiceDate", "TransactionDate", "date"],
        "total": ["total", "InvoiceTotal", "TotalAmount", "total_amount"],
        "tax": ["tax", "TaxAmount", "tax_amount"],
        "currency": ["currency", "Currency", "currency_code"],
    }

    for field_name, possible_keys in field_mappings.items():
        for key in possible_keys:
            if key in response_data and response_data[key] is not None:
                setattr(extracted, field_name, response_data[key])
                break

    line_items_data = response_data.get("line_items", []) or response_data.get(
        "items", []
    )
    for item_data in line_items_data:
        if isinstance(item_data, dict):
            line_item = LineItem(
                description=item_data.get("description", ""),
                quantity=item_data.get("quantity"),
                unit_price=item_data.get("unit_price"),
                amount=item_data.get("amount") or item_data.get("price"),
                confidence=item_data.get("confidence", 1.0),
            )
            extracted.line_items.append(line_item)

    extracted.raw_data = response_data
    extracted.confidence_scores = response_data.get("confidence_scores", {})

    return extracted
