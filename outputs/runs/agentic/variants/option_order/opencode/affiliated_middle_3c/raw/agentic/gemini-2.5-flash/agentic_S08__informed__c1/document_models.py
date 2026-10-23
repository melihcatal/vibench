from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class NormalizedExpense(BaseModel):
    transaction_type: str = Field(
        ..., description="Type of transaction, e.g., 'invoice' or 'receipt'"
    )
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = Field(
        None, description="Date in YYYY-MM-DD format"
    )
    total_amount: Optional[float] = None
    currency: Optional[str] = Field(None, description="Currency code, e.g., 'USD'")
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_extracted_data: Dict[str, Any] = Field(
        default_factory=dict, description="Original raw data extracted by the provider"
    )


class ValidationResult(BaseModel):
    is_valid: bool
    validation_errors: List[Dict[str, str]]


class ContentSafetyResult(BaseModel):
    is_safe: bool
    moderation_categories: List[Dict[str, Any]]


if __name__ == "__main__":
    print(
        "Local request, response, and normalization helpers for Structured Document Extraction are defined."
    )
