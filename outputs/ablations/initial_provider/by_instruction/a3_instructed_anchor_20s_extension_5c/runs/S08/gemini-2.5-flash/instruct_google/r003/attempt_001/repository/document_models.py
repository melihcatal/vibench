import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

class DocumentExtractionResult(BaseModel):
    vendor_name: Optional[str] = None
    document_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_response: Dict[str, Any]

class ExpenseNormalizationSchema(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    document_type: Optional[str] = None
    validation_status: Optional[str] = None
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
