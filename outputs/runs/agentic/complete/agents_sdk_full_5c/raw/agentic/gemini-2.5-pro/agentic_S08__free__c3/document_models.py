from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class InvoiceLineItem(BaseModel):
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    amount: Optional[float]


class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str]
    invoice_id: Optional[str]
    invoice_date: Optional[str]
    due_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    line_items: List[InvoiceLineItem] = []
    raw_fields: Dict[str, Any] = {}


class ReceiptItem(BaseModel):
    description: str
    quantity: Optional[float]
    total_price: Optional[float]


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str]
    transaction_date: Optional[str]
    transaction_time: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    items: List[ReceiptItem] = []
    raw_fields: Dict[str, Any] = {}


class NormalizedExpenseItem(BaseModel):
    item_id: Optional[str] = None
    description: str
    amount: float
    category: Optional[str] = "Uncategorized"


class NormalizedExpense(BaseModel):
    expense_id: str
    vendor: str
    transaction_date: str
    total: float
    currency_code: str = "USD"
    expense_type: str  # e.g., 'INVOICE', 'RECEIPT'
    items: List[NormalizedExpenseItem] = []
    notes: Optional[str] = None
    source_document_id: str
