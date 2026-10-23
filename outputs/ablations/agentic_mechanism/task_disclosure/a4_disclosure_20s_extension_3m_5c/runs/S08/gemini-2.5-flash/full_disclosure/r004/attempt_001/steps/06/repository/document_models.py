from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DocumentExtractionRequest:
    """
    Represents a request for structured document extraction.
    """
    document_content: str
    document_type: str
    # Add any other relevant request parameters here, e.g., output_format, specific_fields_to_extract

@dataclass
class ExtractedField:
    """
    Represents a single extracted field from a document.
    """
    field_name: str
    field_value: str
    confidence: float
    page_number: Optional[int] = None

@dataclass
class DocumentExtractionResponse:
    """
    Represents the response from a structured document extraction operation.
    """
    document_id: str
    extracted_fields: List[ExtractedField] = field(default_factory=list)
    # Add any other relevant response parameters here, e.g., raw_text, errors, warnings

@dataclass
class NormalizedExpenseItem:
    """
    Represents a normalized line item within an expense.
    """
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: float

@dataclass
class NormalizedExpense:
    """
    Represents a normalized expense record in a standard JSON schema.
    """
    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str
    tax_amount: Optional[float] = None
    items: List[NormalizedExpenseItem] = field(default_factory=list)
    notes: Optional[str] = None
    # Add any other common expense fields for normalization
