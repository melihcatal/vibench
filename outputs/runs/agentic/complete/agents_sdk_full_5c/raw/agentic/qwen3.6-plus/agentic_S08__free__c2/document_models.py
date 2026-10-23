"""Define local request, response, and normalization helpers for Structured Document Extraction."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: float = 0.0


class InvoiceExtraction(BaseModel):
    vendor: str = ""
    invoice_date: str = ""
    total: float = 0.0
    tax: Optional[float] = None
    line_items: List[LineItem] = []
    confidence: float = 0.0
    raw_text: Optional[str] = None


class ReceiptExtraction(BaseModel):
    merchant: str = ""
    transaction_date: str = ""
    total: float = 0.0
    tax: Optional[float] = None
    items: List[LineItem] = []
    confidence: float = 0.0
    raw_text: Optional[str] = None


class NormalizedExpense(BaseModel):
    entity_name: str = ""
    document_type: str = ""
    transaction_date: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}
    validation_status: str = "pending"
    created_at: Optional[str] = None


class DocumentValidationResult(BaseModel):
    is_valid: bool = False
    missing_fields: List[str] = []
    low_confidence_fields: List[str] = []
    overall_confidence: float = 0.0
    errors: List[str] = []
    field_details: Dict[str, Any] = {}


def parse_line_item_from_dict(data: Dict[str, Any]) -> LineItem:
    return LineItem(
        description=data.get("description", ""),
        quantity=data.get("quantity"),
        unit_price=data.get("unit_price"),
        total=float(data.get("total", 0.0))
    )


def normalize_confidence_score(raw_score: float, provider: str = "generic") -> float:
    if provider == "aws_textract":
        return max(0.0, min(1.0, raw_score))
    elif provider == "google_document_ai":
        return max(0.0, min(1.0, raw_score))
    elif provider == "azure_form_recognizer":
        return max(0.0, min(1.0, raw_score))
    return max(0.0, min(1.0, raw_score))


def build_extraction_metadata(
    provider: str,
    confidence: float,
    processing_time_ms: Optional[float] = None,
    page_count: int = 1
) -> Dict[str, Any]:
    metadata = {
        "extraction_provider": provider,
        "confidence": confidence,
        "page_count": page_count,
        "extracted_at": datetime.utcnow().isoformat()
    }
    if processing_time_ms is not None:
        metadata["processing_time_ms"] = processing_time_ms
    return metadata
