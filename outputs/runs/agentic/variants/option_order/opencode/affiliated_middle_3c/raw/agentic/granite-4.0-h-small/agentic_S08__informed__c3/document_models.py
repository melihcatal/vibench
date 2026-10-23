from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InvoiceRequest:
    file_bytes: bytes
    document_type: str = "invoice"


@dataclass
class InvoiceResponse:
    vendor: Optional[str]
    date: Optional[str]
    total: Optional[str]
    items: List[str] = dataclass.field(default_factory=list)


@dataclass
class ReceiptRequest:
    file_bytes: bytes
    document_type: str = "receipt"


@dataclass
class ReceiptResponse:
    merchant: Optional[str]
    tax: Optional[str]
    total: Optional[str]
    items: List[str] = dataclass.field(default_factory=list)


# Simple normalization helper
def to_standard_json(raw):
    # Convert extracted fields to a uniform schema
    return {
        "vendor": raw.get("vendor"),
        "date": raw.get("date"),
        "total": raw.get("total"),
        "items": raw.get("items", []),
        "normalized_at": datetime.utcnow().isoformat() + "Z",
    }
