from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json


@dataclass
class InvoiceExtractionRequest:
    """Request model for invoice extraction."""

    file_path: str
    model_id: str = "prebuilt-invoice"
    include_line_items: bool = True
    include_tax_details: bool = True
    confidence_threshold: float = 0.7


@dataclass
class ReceiptExtractionRequest:
    """Request model for receipt extraction."""

    file_path: str
    processor_id: Optional[str] = None
    mime_type: str = "image/jpeg"
    include_items: bool = True


@dataclass
class ExtractionResponse:
    """Base response model for document extraction."""

    success: bool
    extracted_data: Dict[str, Any]
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None


@dataclass
class InvoiceExtractionResponse(ExtractionResponse):
    """Response model for invoice extraction."""

    vendor: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    tax_amount: Optional[float] = None


@dataclass
class ReceiptExtractionResponse(ExtractionResponse):
    """Response model for receipt extraction."""

    merchant: Optional[str] = None
    receipt_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    items: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExpenseRecord:
    """Normalized expense record model."""

    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    tax_amount: Optional[float] = None
    category: str = "uncategorized"
    source_type: str = "invoice"
    extraction_source: str = "unknown"
    normalized_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpense:
    """Container for normalized expense data."""

    record: ExpenseRecord
    validation_result: Optional[Dict[str, Any]] = None
    original_data: Optional[Dict[str, Any]] = None


@dataclass
class ValidationResult:
    """Validation result model."""

    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[Dict[str, Any]] = field(default_factory=list)
    field_details: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    validation_timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    warnings: List[str] = field(default_factory=list)


class DocumentModels:
    """Helper class for document model operations."""

    @staticmethod
    def expense_record_to_dict(record: ExpenseRecord) -> Dict[str, Any]:
        """Convert ExpenseRecord to dictionary."""
        return {
            "vendor_name": record.vendor_name,
            "transaction_date": record.transaction_date,
            "total_amount": record.total_amount,
            "currency": record.currency,
            "line_items": record.line_items,
            "tax_amount": record.tax_amount,
            "category": record.category,
            "source_type": record.source_type,
            "extraction_source": record.extraction_source,
            "normalized_at": record.normalized_at,
            "metadata": record.metadata,
        }

    @staticmethod
    def dict_to_expense_record(data: Dict[str, Any]) -> ExpenseRecord:
        """Convert dictionary to ExpenseRecord."""
        return ExpenseRecord(
            vendor_name=data.get("vendor_name", ""),
            transaction_date=data.get("transaction_date", ""),
            total_amount=data.get("total_amount", 0.0),
            currency=data.get("currency", "USD"),
            line_items=data.get("line_items", []),
            tax_amount=data.get("tax_amount"),
            category=data.get("category", "uncategorized"),
            source_type=data.get("source_type", "invoice"),
            extraction_source=data.get("extraction_source", "unknown"),
            normalized_at=data.get("normalized_at", datetime.utcnow().isoformat()),
            metadata=data.get("metadata", {}),
        )

    @staticmethod
    def normalize_line_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a line item to standard format."""
        normalized = {
            "description": item.get("description", item.get("item_description", "")),
            "quantity": float(item.get("quantity", item.get("qty", 1))),
            "unit_price": float(item.get("unit_price", item.get("price", 0))),
            "amount": float(item.get("amount", item.get("total", 0))),
        }

        # Calculate amount if not provided
        if (
            normalized["amount"] == 0
            and normalized["quantity"] > 0
            and normalized["unit_price"] > 0
        ):
            normalized["amount"] = normalized["quantity"] * normalized["unit_price"]

        return normalized

    @staticmethod
    def calculate_totals(expense: ExpenseRecord) -> Dict[str, float]:
        """Calculate various totals from expense record."""
        subtotal = sum(item.get("amount", 0) for item in expense.line_items)
        tax = expense.tax_amount or 0
        total = expense.total_amount or (subtotal + tax)

        return {
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "item_count": len(expense.line_items),
        }


def create_extraction_request(
    file_type: str, **kwargs
) -> Union[InvoiceExtractionRequest, ReceiptExtractionRequest]:
    """Factory method to create extraction request based on file type."""
    if file_type.lower() in ["invoice", "inv"]:
        return InvoiceExtractionRequest(**kwargs)
    elif file_type.lower() in ["receipt", "rcpt"]:
        return ReceiptExtractionRequest(**kwargs)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
