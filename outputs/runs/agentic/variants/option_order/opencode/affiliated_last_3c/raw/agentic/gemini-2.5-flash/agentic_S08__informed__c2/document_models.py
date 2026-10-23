import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, conlist, NonNegativeFloat, confloat


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[NonNegativeFloat] = None
    unit_price: Optional[NonNegativeFloat] = None
    total_price: Optional[NonNegativeFloat] = None
    currency: Optional[str] = None


class DocumentField(BaseModel):
    value: Optional[Any] = None
    confidence: confloat(ge=0.0, le=1.0) = 0.0


class ExtractedInvoice(BaseModel):
    vendor_name: DocumentField[str] = Field(default_factory=DocumentField)
    invoice_date: DocumentField[datetime.date] = Field(default_factory=DocumentField)
    total_amount: DocumentField[NonNegativeFloat] = Field(default_factory=DocumentField)
    currency: DocumentField[str] = Field(default_factory=DocumentField)
    line_items: List[LineItem] = []
    notes: Optional[DocumentField[str]] = Field(default_factory=DocumentField)


class ExtractedReceipt(BaseModel):
    merchant_name: DocumentField[str] = Field(default_factory=DocumentField)
    receipt_date: DocumentField[datetime.date] = Field(default_factory=DocumentField)
    total_amount: DocumentField[NonNegativeFloat] = Field(default_factory=DocumentField)
    tax_amount: DocumentField[NonNegativeFloat] = Field(default_factory=DocumentField)
    currency: DocumentField[str] = Field(default_factory=DocumentField)
    line_items: List[LineItem] = []


class NormalizedExpense(BaseModel):
    document_type: str = Field(
        ..., description="Type of the document, e.g., 'invoice' or 'receipt'"
    )
    vendor_name: Optional[str] = None
    transaction_date: Optional[datetime.date] = None
    total_amount: Optional[NonNegativeFloat] = None
    currency: Optional[str] = None
    tax_amount: Optional[NonNegativeFloat] = None
    line_items: List[LineItem] = []
    notes: Optional[str] = None
    raw_extraction: Dict[str, Any] = Field(
        default_factory=dict, description="Raw data from the extraction service"
    )


class ValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    extracted_value: Optional[Any] = None
    confidence: Optional[float] = None


class DocumentValidationResponse(BaseModel):
    is_document_valid: bool
    validation_details: List[ValidationResult]
