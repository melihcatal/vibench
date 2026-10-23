from typing import Dict, Any, List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, validator


class LineItem(BaseModel):
    """Model for expense line items."""

    description: str
    quantity: float = 1.0
    unit_price: float = 0.0
    total: float = 0.0

    @validator("total", pre=True, always=True)
    def calculate_total(cls, v, values):
        if v is None or v == 0:
            quantity = values.get("quantity", 1.0)
            unit_price = values.get("unit_price", 0.0)
            return quantity * unit_price
        return v


class ExpenseRecord(BaseModel):
    """Standardized expense record model."""

    expense_id: str
    source_type: str = Field(..., regex="^(invoice|receipt)$")
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total_amount: float = Field(..., ge=0)
    tax_amount: float = Field(default=0.0, ge=0)
    currency: str = "USD"
    line_items: List[LineItem] = []
    metadata: Dict[str, Any] = {}

    @validator("date")
    def validate_date(cls, v):
        if v:
            try:
                datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                try:
                    date.fromisoformat(v)
                except ValueError:
                    raise ValueError(f"Invalid date format: {v}")
        return v


class ExtractionRequest(BaseModel):
    """Request model for document extraction."""

    document_path: str
    document_type: str = Field(..., regex="^(invoice|receipt)$")
    include_line_items: bool = True
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)


class ExtractionResponse(BaseModel):
    """Response model for document extraction."""

    success: bool
    extracted_data: Dict[str, Any]
    confidence_scores: Dict[str, float]
    validation_results: Dict[str, Any]
    error_message: Optional[str] = None


class NormalizationRequest(BaseModel):
    """Request model for expense normalization."""

    extracted_data: Dict[str, Any]
    source_type: str = Field(..., regex="^(invoice|receipt)$")
    currency: str = "USD"
    additional_metadata: Dict[str, Any] = {}


class ValidationResult(BaseModel):
    """Model for field validation results."""

    field_name: str
    is_present: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    value: Optional[Any] = None
    warning: Optional[str] = None


class DocumentValidationResponse(BaseModel):
    """Response model for document validation."""

    is_valid: bool
    required_fields: List[str]
    missing_fields: List[str]
    confidence_scores: Dict[str, float]
    field_validations: Dict[str, ValidationResult]
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
