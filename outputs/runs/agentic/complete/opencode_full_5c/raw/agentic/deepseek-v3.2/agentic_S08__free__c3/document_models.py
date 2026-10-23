from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    amount: float

    def to_dict(self):
        return asdict(self)


@dataclass
class ExpenseRecord:
    vendor: str
    date: str
    total_amount: float
    document_type: str
    line_items: List[LineItem]
    tax_amount: float
    currency: str
    notes: Optional[str] = None
    confidence_score: Optional[float] = None
    source_file: Optional[str] = None
    extracted_at: Optional[str] = None

    def __post_init__(self):
        if self.extracted_at is None:
            self.extracted_at = datetime.now().isoformat()

    def to_dict(self):
        result = asdict(self)
        result["line_items"] = [item.to_dict() for item in self.line_items]
        return result


@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: List[str]
    confidence_scores: Dict[str, float]
    required_fields: List[Dict[str, Any]]

    def to_dict(self):
        return asdict(self)


@dataclass
class ExtractionRequest:
    file_path: str
    document_type: str
    include_raw_text: bool = False
    confidence_threshold: float = 0.5

    def to_dict(self):
        return asdict(self)


@dataclass
class ExtractionResponse:
    success: bool
    extracted_data: Dict[str, Any]
    normalized_data: Optional[Dict[str, Any]] = None
    validation_result: Optional[ValidationResult] = None
    error_message: Optional[str] = None

    def to_dict(self):
        result = asdict(self)
        if self.validation_result:
            result["validation_result"] = self.validation_result.to_dict()
        return result
