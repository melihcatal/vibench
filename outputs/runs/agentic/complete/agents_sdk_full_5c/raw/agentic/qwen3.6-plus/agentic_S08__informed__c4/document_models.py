"""
Define local request, response, and normalization helpers for Structured Document Extraction.

Contains dataclasses and helpers for building extraction requests,
parsing provider responses, and normalizing into a common schema.
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import json


@dataclass
class ExtractedField:
    """Represents a single extracted field from a document."""
    name: str
    value: Any
    confidence: float = 1.0
    bounding_box: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name, "value": self.value, "confidence": self.confidence}
        if self.bounding_box:
            result["bounding_box"] = self.bounding_box
        return result


@dataclass
class LineItem:
    """Represents a single line item from an invoice or receipt."""
    description: str = ""
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    tax_amount: Optional[float] = None
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "tax_amount": self.tax_amount,
            "confidence": self.confidence,
        }
        return {k: v for k, v in result.items() if v is not None or k == "description"}


@dataclass
class InvoiceExtractionResult:
    """Standardized result from invoice field extraction."""
    vendor_name: Optional[str] = None
    vendor_confidence: float = 0.0
    invoice_number: Optional[str] = None
    invoice_number_confidence: float = 0.0
    invoice_date: Optional[str] = None
    invoice_date_confidence: float = 0.0
    total_amount: Optional[float] = None
    total_confidence: float = 0.0
    tax_amount: Optional[float] = None
    tax_confidence: float = 0.0
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    provider: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor_name": self.vendor_name,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "line_items": [item.to_dict() for item in self.line_items],
            "provider": self.provider,
        }


@dataclass
class ReceiptExtractionResult:
    """Standardized result from receipt field extraction."""
    merchant_name: Optional[str] = None
    merchant_confidence: float = 0.0
    receipt_date: Optional[str] = None
    receipt_date_confidence: float = 0.0
    total_amount: Optional[float] = None
    total_confidence: float = 0.0
    tax_amount: Optional[float] = None
    tax_confidence: float = 0.0
    items: List[LineItem] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None
    provider: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "merchant_name": self.merchant_name,
            "receipt_date": self.receipt_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "items": [item.to_dict() for item in self.items],
            "provider": self.provider,
        }


@dataclass
class NormalizedExpense:
    """Normalized expense record conforming to a standard JSON schema."""
    expense_id: Optional[str] = None
    expense_type: str = ""
    source_document_type: str = ""
    vendor_or_merchant: Optional[str] = None
    document_date: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    currency: str = "USD"
    confidence: float = 0.0
    validation_status: str = "pending"
    raw_extraction: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(asdict(self), indent=2, default=str)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return asdict(self)


class ExtractionRequest:
    """Helper to build extraction requests for various providers."""

    @staticmethod
    def build_from_file(file_path: str, file_type: str = "invoice") -> Dict[str, Any]:
        """Build a request dict from a local file path."""
        return {
            "file_path": file_path,
            "file_type": file_type,
        }

    @staticmethod
    def build_from_bytes(file_bytes: bytes, file_type: str = "invoice") -> Dict[str, Any]:
        """Build a request dict from raw file bytes."""
        return {
            "file_bytes": file_bytes,
            "file_type": file_type,
        }

    @staticmethod
    def build_from_url(file_url: str, file_type: str = "invoice") -> Dict[str, Any]:
        """Build a request dict from a file URL."""
        return {
            "file_url": file_url,
            "file_type": file_type,
        }


def parse_provider_confidence(raw: Dict[str, Any], field_name: str) -> float:
    """Extract confidence score from a provider response for a given field."""
    field_data = raw.get(field_name, {})
    if isinstance(field_data, dict):
        conf = field_data.get("confidence", field_data.get("probability", 1.0))
        if isinstance(conf, (int, float)):
            return float(conf)
    return 1.0


def build_normalized_expense_from_invoice(
    invoice_result: InvoiceExtractionResult,
    expense_id: Optional[str] = None,
) -> NormalizedExpense:
    """Build a NormalizedExpense from an InvoiceExtractionResult."""
    avg_confidence = 0.0
    confidences = [
        invoice_result.vendor_confidence,
        invoice_result.invoice_date_confidence,
        invoice_result.total_confidence,
        invoice_result.tax_confidence,
    ]
    confidences = [c for c in confidences if c > 0]
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)

    line_items_dicts = [item.to_dict() for item in invoice_result.line_items]

    return NormalizedExpense(
        expense_id=expense_id,
        expense_type="invoice",
        source_document_type="invoice",
        vendor_or_merchant=invoice_result.vendor_name,
        document_date=invoice_result.invoice_date,
        subtotal=invoice_result.total_amount - (invoice_result.tax_amount or 0),
        tax=invoice_result.tax_amount,
        total=invoice_result.total_amount,
        line_items=line_items_dicts,
        confidence=round(avg_confidence, 4),
        validation_status="pending",
        raw_extraction=invoice_result.to_dict(),
    )


def build_normalized_expense_from_receipt(
    receipt_result: ReceiptExtractionResult,
    expense_id: Optional[str] = None,
) -> NormalizedExpense:
    """Build a NormalizedExpense from a ReceiptExtractionResult."""
    avg_confidence = 0.0
    confidences = [
        receipt_result.merchant_confidence,
        receipt_result.receipt_date_confidence,
        receipt_result.total_confidence,
        receipt_result.tax_confidence,
    ]
    confidences = [c for c in confidences if c > 0]
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)

    items_dicts = [item.to_dict() for item in receipt_result.items]

    return NormalizedExpense(
        expense_id=expense_id,
        expense_type="receipt",
        source_document_type="receipt",
        vendor_or_merchant=receipt_result.merchant_name,
        document_date=receipt_result.receipt_date,
        subtotal=receipt_result.total_amount - (receipt_result.tax_amount or 0),
        tax=receipt_result.tax_amount,
        total=receipt_result.total_amount,
        line_items=items_dicts,
        confidence=round(avg_confidence, 4),
        validation_status="pending",
        raw_extraction=receipt_result.to_dict(),
    )
