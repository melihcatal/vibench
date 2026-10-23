# [HELPER] document_models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class InvoiceExtractionResponse(BaseModel):
    vendor: str = Field(..., description='Vendor/business name')
    date: str = Field(..., description='Invoice date (YYYY-MM-DD)')
    total: str = Field(..., description='Total amount as string')
    line_items: List[dict] = Field(default_factory=list, description='Extracted line-item details')

class ReceiptExtractionResponse(BaseModel):
    merchant: str = Field(..., description='Merchant/business name')
    tax: Optional[str] = Field(default=None, description='Tax amount as string')
    total: str = Field(..., description='Total amount as string')
    items: List[dict] = Field(default_factory=list, description='Extracted item details')
# Optional generic base if needed later
class ExtractionBase(BaseModel, extra='forbid'):
    pass
# Normalized schema used by later steps
from normalize_expense import NormalizedExpense  # imported at runtime