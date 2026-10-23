from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class Invoice(BaseModel):
    vendor: str
    date: date
    total: float
    line_items: List[LineItem] = Field(default_factory=list)

class Item(BaseModel):
    description: str
    quantity: float
    price: float

class Receipt(BaseModel):
    merchant: str
    tax: float
    total: float
    items: List[Item] = Field(default_factory=list)

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: str
    transaction_date: date
    total_amount: float
    currency: str
    line_items: Optional[List[Dict[str, Any]]] = None
    original_data: Dict[str, Any]

class FieldValidation(BaseModel):
    field_name: str
    is_valid: bool
    confidence: float
    message: Optional[str] = None

class DocumentValidationResult(BaseModel):
    document_id: str
    is_document_valid: bool
    validation_details: List[FieldValidation]
