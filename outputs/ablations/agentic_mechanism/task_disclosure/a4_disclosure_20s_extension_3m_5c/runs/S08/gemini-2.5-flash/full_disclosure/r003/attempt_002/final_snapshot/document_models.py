import dataclasses
from typing import Dict, List, Optional, Union

@dataclasses.dataclass
class DocumentExtractionRequest:
    document_content: bytes
    mime_type: Optional[str] = None

@dataclasses.dataclass
class DocumentExtractionResponse:
    extracted_fields: Dict[str, Union[str, float, List[Dict]]]
    document_type: str

@dataclasses.dataclass
class NormalizedExpenseLineItem:
    description: str
    amount: float
    quantity: Optional[int] = None

@dataclasses.dataclass
class NormalizedExpense:
    vendor_name: str
    transaction_date: str
    total_amount: float
    line_items: List[NormalizedExpenseLineItem]