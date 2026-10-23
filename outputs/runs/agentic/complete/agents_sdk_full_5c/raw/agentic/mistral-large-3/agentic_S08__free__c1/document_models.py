from pydantic import BaseModel
from typing import List, Optional


class LineItem(BaseModel):
    description: str
    amount: str


class InvoiceExtractionResponse(BaseModel):
    vendor: str
    date: str
    total: str
    line_items: List[LineItem]


class ReceiptItem(BaseModel):
    description: str
    amount: str


class ReceiptExtractionResponse(BaseModel):
    merchant: str
    tax: Optional[str]
    total: str
    items: List[ReceiptItem]