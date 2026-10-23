from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, validator
import json


# Request Models
class DocumentExtractionRequest(BaseModel):
    """Base request model for document extraction."""

    document_bytes: bytes
    document_type: str = Field(
        ..., description="Type of document: invoice, receipt, etc."
    )
    extraction_options: Dict[str, Any] = Field(default_factory=dict)


class InvoiceExtractionRequest(DocumentExtractionRequest):
    """Request model for invoice extraction."""

    document_type: str = "invoice"
    extract_line_items: bool = True
    extract_vendor_details: bool = True


class ReceiptExtractionRequest(DocumentExtractionRequest):
    """Request model for receipt extraction."""

    document_type: str = "receipt"
    extract_items: bool = True
    extract_tax_details: bool = True


# Response Models
class DocumentExtractionResponse(BaseModel):
    """Base response model for document extraction."""

    extracted_fields: Dict[str, Any]
    confidence: Optional[float] = None
    provider: str
    model: str
    processing_time_ms: Optional[int] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class InvoiceExtractionResponse(DocumentExtractionResponse):
    """Response model for invoice extraction."""

    vendor_details: Optional[Dict[str, Any]] = None
    line_items: List[Dict[str, Any]] = Field(default_factory=list)


class ReceiptExtractionResponse(DocumentExtractionResponse):
    """Response model for receipt extraction."""

    merchant_details: Optional[Dict[str, Any]] = None
    items: List[Dict[str, Any]] = Field(default_factory=list)
    tax_details: Optional[Dict[str, Any]] = None


# Normalization Models
class LineItem(BaseModel):
    """Model for a line item in an expense."""

    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    category: Optional[str] = None


class ExpenseRecord(BaseModel):
    """Normalized expense record model."""

    vendor_name: str
    transaction_date: str  # ISO 8601 date string
    total_amount: float
    currency: str = "USD"
    category: str = Field(
        default="other",
        description="Category: office_supplies, travel, meals, software, hardware, services, utilities, other",
    )
    line_items: List[LineItem] = Field(default_factory=list)
    tax_amount: Optional[float] = None
    tax_rate: Optional[float] = None
    payment_method: str = Field(
        default="credit_card",
        description="Payment method: credit_card, cash, bank_transfer, check, other",
    )
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @validator("category")
    def validate_category(cls, v):
        valid_categories = [
            "office_supplies",
            "travel",
            "meals",
            "software",
            "hardware",
            "services",
            "utilities",
            "other",
        ]
        if v not in valid_categories:
            return "other"
        return v

    @validator("payment_method")
    def validate_payment_method(cls, v):
        valid_methods = ["credit_card", "cash", "bank_transfer", "check", "other"]
        if v not in valid_methods:
            return "credit_card"
        return v


class NormalizedExpense(BaseModel):
    """Wrapper for normalized expense with metadata."""

    expense: ExpenseRecord
    normalization_provider: str
    normalization_model: str
    original_document_type: str
    confidence_score: Optional[float] = None
    validation_status: str = "pending"


# Validation Models
class ValidationResult(BaseModel):
    """Model for validation results."""

    is_valid: bool
    missing_fields: List[str] = Field(default_factory=list)
    low_confidence_fields: List[str] = Field(default_factory=list)
    validation_details: Dict[str, Any] = Field(default_factory=dict)
    provider: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# Helper functions
def serialize_for_json(obj: Any) -> Any:
    """Serialize objects for JSON output."""
    if isinstance(obj, BaseModel):
        return obj.dict()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        return obj.hex()
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    return obj


def create_extraction_payload(document_path: str, document_type: str) -> Dict[str, Any]:
    """Create a payload for document extraction."""
    with open(document_path, "rb") as f:
        document_bytes = f.read()

    if document_type == "invoice":
        return InvoiceExtractionRequest(
            document_bytes=document_bytes, document_type=document_type
        ).dict()
    elif document_type == "receipt":
        return ReceiptExtractionRequest(
            document_bytes=document_bytes, document_type=document_type
        ).dict()
    else:
        return DocumentExtractionRequest(
            document_bytes=document_bytes, document_type=document_type
        ).dict()


def parse_extraction_response(
    response_data: Dict[str, Any], document_type: str
) -> DocumentExtractionResponse:
    """Parse extraction response based on document type."""
    if document_type == "invoice":
        return InvoiceExtractionResponse(**response_data)
    elif document_type == "receipt":
        return ReceiptExtractionResponse(**response_data)
    else:
        return DocumentExtractionResponse(**response_data)


# Data classes for internal use
@dataclass
class FieldExtraction:
    """Data class for field extraction results."""

    name: str
    value: Any
    confidence: float
    source: str


@dataclass
class DocumentMetadata:
    """Data class for document metadata."""

    document_type: str
    file_size: int
    mime_type: str
    extraction_timestamp: datetime = field(default_factory=datetime.utcnow)
    processing_id: Optional[str] = None
