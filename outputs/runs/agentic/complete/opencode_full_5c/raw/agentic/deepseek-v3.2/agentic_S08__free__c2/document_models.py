from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from datetime import datetime


class ExpenseCategory(Enum):
    TRAVEL = "travel"
    MEALS = "meals"
    OFFICE_SUPPLIES = "office_supplies"
    SOFTWARE = "software"
    HARDWARE = "hardware"
    SERVICES = "services"
    UTILITIES = "utilities"
    RENT = "rent"
    TRANSPORTATION = "transportation"
    OTHER = "other"


@dataclass
class InvoiceExtractionRequest:
    image_path: str
    invoice_type: str = "standard"
    extract_line_items: bool = True


@dataclass
class ReceiptExtractionRequest:
    image_path: str
    receipt_type: str = "standard"
    extract_items: bool = True


@dataclass
class InvoiceExtractionResult:
    vendor: str
    invoice_date: str
    total_amount: str
    line_items: List[Dict[str, Any]]
    raw_fields: Dict[str, Any]
    confidence_scores: Dict[str, float]
    provider: str
    model_used: str
    extraction_timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class ReceiptExtractionResult:
    merchant: str
    tax_amount: Optional[float]
    total_amount: Optional[float]
    items: List[Dict[str, Any]]
    raw_text: str
    confidence_scores: Dict[str, float]
    provider: str
    model_used: str
    extraction_timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class ValidationRule:
    field: str
    required: bool = True
    min_confidence: float = 0.7
    validation_type: str = "presence_and_confidence"


@dataclass
class ValidationResult:
    is_valid: bool
    validation_errors: List[str]
    warnings: List[str]
    validated_fields: Dict[str, Dict[str, Any]]
    confidence_scores: Dict[str, float]
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class NormalizedExpense:
    vendor: str
    amount: float
    date: str
    description: str
    category: ExpenseCategory
    subcategory: Optional[str]
    tags: List[str]
    line_items: List[Dict[str, Any]]
    source_provider: str
    source_model: str
    confidence_scores: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    normalization_timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class ExpenseSummary:
    vendor: str
    total_amount: float
    category: ExpenseCategory
    line_item_count: int
    date_range: Optional[Dict[str, str]]
    summary_text: str
    provider: str
    model_used: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    summary_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SafetyCheckResult:
    is_safe: bool
    flagged_categories: List[str]
    confidence_scores: Dict[str, float]
    provider: str
    model_used: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    check_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    provider: str
    model_used: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    translation_timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


@dataclass
class StorageResult:
    document_id: str
    storage_location: str
    success: bool
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    storage_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
