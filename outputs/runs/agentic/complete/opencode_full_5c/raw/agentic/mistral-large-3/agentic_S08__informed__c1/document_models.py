from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: float = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)
    total_price: float = Field(..., ge=0)


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_or_merchant: Optional[str]
    date: Optional[str]
    total_amount: float = Field(..., ge=0)
    tax_amount: float = Field(0, ge=0)
    items: List[LineItem] = []
    confidence_score: float = Field(..., ge=0, le=1)
    currency: str = "USD"


class ExtractionResponse(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: List[Dict[str, Any]] = []
    confidence: float = Field(0, ge=0, le=1)
    merchant: Optional[str] = None
    tax: Optional[float] = None
    items: List[Dict[str, Any]] = []


def parse_extraction_response(data: Dict[str, Any]) -> ExtractionResponse:
    return ExtractionResponse(**data)
