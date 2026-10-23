from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class DocumentField(BaseModel):
    value: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    currency: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class InvoiceExtractionResult(BaseModel):
    vendor_name: DocumentField
    invoice_date: DocumentField
    total_amount: DocumentField
    line_items: List[LineItem] = Field(default_factory=list)
    currency: DocumentField
    purchase_order: Optional[DocumentField] = None
    vendor_address: Optional[DocumentField] = None
    due_date: Optional[DocumentField] = None
    invoice_id: Optional[DocumentField] = None
    notes: Optional[DocumentField] = None


class ReceiptExtractionResult(BaseModel):
    merchant_name: DocumentField
    transaction_date: DocumentField
    total_amount: DocumentField
    tax_amount: Optional[DocumentField] = None
    line_items: List[LineItem] = Field(default_factory=list)
    currency: DocumentField
    receipt_id: Optional[DocumentField] = None


class NormalizedExpense(BaseModel):
    document_type: str  # e.g., "invoice", "receipt"
    vendor_name: str
    transaction_date: str  # ISO 8601 format
    total_amount: float
    currency: str
    tax_amount: Optional[float] = None
    line_items: List[Dict] = Field(default_factory=list)
    notes: Optional[str] = None
    original_document_id: Optional[str] = None
    extracted_fields: Dict = Field(
        default_factory=dict
    )  # Original raw extracted fields for reference


class ValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    extracted_value: Optional[str] = None
    expected_confidence: Optional[float] = None
    actual_confidence: Optional[float] = None
