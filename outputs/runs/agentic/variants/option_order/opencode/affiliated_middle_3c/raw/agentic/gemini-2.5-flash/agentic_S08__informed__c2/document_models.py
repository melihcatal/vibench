import json
from pydantic import BaseModel, Field, conlist, confloat
from typing import Optional, List, Dict, Any


class InvoiceLineItem(BaseModel):
    description: str
    quantity: Optional[float]
    unit_price: Optional[float]
    total_price: Optional[float]


class ReceiptItem(BaseModel):
    description: str
    quantity: Optional[float]
    price: Optional[float]


class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    invoice_total: Optional[confloat(ge=0)]
    line_items: Optional[List[InvoiceLineItem]]


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str]
    tax_amount: Optional[confloat(ge=0)]
    total_amount: Optional[confloat(ge=0)]
    items: Optional[List[ReceiptItem]]


class NormalizedExpense(BaseModel):
    document_type: str = Field(..., pattern="^(invoice|receipt)$")
    vendor_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[confloat(ge=0)]
    currency: Optional[str] = "USD"
    line_items: Optional[List[Dict[str, Any]]]
    original_data: Dict[str, Any]


class DocumentValidationResult(BaseModel):
    field_name: str
    is_present: bool
    confidence: Optional[float]
    message: Optional[str]


class DocumentValidationResponse(BaseModel):
    is_valid: bool
    validation_results: List[DocumentValidationResult]
