from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union, Dict, Any


class Confidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float = Field(..., ge=0.0, le=1.0)


class ExtractedField(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str
    confidence: Confidence


class LineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: float
    confidence: Confidence


class InvoiceExtract(BaseModel):
    model_config = ConfigDict(extra="allow")
    vendor: ExtractedField
    invoice_date: ExtractedField
    total_amount: ExtractedField
    line_items: List[LineItem]
    raw_response: Optional[Dict[str, Any]] = None


class ReceiptExtract(BaseModel):
    model_config = ConfigDict(extra="allow")
    merchant_name: ExtractedField
    transaction_date: ExtractedField
    tax_amount: ExtractedField
    total_amount: ExtractedField
    items: List[LineItem]
    raw_response: Optional[Dict[str, Any]] = None


class NormalizedExpense(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expense_type: str
    vendor_or_merchant: str
    date: str
    tax_amount: Optional[float] = None
    total_amount: float
    line_items: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
