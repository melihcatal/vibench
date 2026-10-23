"""
Local request, response, and normalization helpers for Structured Document Extraction.

Defines Pydantic models for invoice extraction, receipt extraction, expense records,
and validation responses used across the document extraction service integrations.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    """Represents a single line item from an invoice or expense document."""
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    line_total: Optional[float] = None


class InvoiceExtractionRequest(BaseModel):
    """Request model for invoice field extraction."""
    document_path: Optional[str] = None
    document_bytes: Optional[bytes] = None
    aws_region: Optional[str] = None


class InvoiceExtractionResponse(BaseModel):
    """Response model for invoice field extraction via AWS Textract."""
    vendor: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    vendor_confidence: float = 0.0
    date_confidence: float = 0.0
    total_confidence: float = 0.0
    raw_response: Optional[Dict[str, Any]] = None


class ReceiptItem(BaseModel):
    """Represents a single item from a receipt."""
    description: Optional[str] = None
    total_price: Optional[float] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    confidence: float = 0.0


class ReceiptExtractionRequest(BaseModel):
    """Request model for receipt field extraction."""
    document_path: Optional[str] = None
    document_bytes: Optional[bytes] = None
    azure_endpoint: Optional[str] = None
    azure_api_key: Optional[str] = None
    model_id: str = "prebuilt-receipt"


class ReceiptExtractionResponse(BaseModel):
    """Response model for receipt field extraction via Azure Document Intelligence."""
    merchant: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    subtotal_amount: Optional[float] = None
    items: List[ReceiptItem] = Field(default_factory=list)
    merchant_confidence: float = 0.0
    date_confidence: float = 0.0
    total_confidence: float = 0.0
    tax_confidence: float = 0.0


class ExpenseRecord(BaseModel):
    """Standardized expense record for storage and further processing."""
    vendor: Optional[str] = None
    date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: str = "USD"
    line_items: List[LineItem] = Field(default_factory=list)
    document_type: str = "expense_document"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class NormalizedExpenseRequest(BaseModel):
    """Request model for expense normalization."""
    project_id: Optional[str] = None
    location: Optional[str] = None
    processor_id: Optional[str] = None
    document_path: Optional[str] = None
    document_bytes: Optional[bytes] = None
    mime_type: str = "application/pdf"
    extracted_data: Optional[Dict[str, Any]] = None


class NormalizedExpenseResponse(BaseModel):
    """Response model for expense normalization via Google Cloud Document AI."""
    expense: ExpenseRecord
    normalized: bool = True


class FieldValidation(BaseModel):
    """Validation result for a single extracted field."""
    field_name: str
    is_valid: bool
    confidence: float = 0.0
    error: Optional[str] = None


class ValidationRequest(BaseModel):
    """Request model for document field validation."""
    extracted_data: Dict[str, Any]
    required_fields: Optional[List[str]] = None
    min_confidence: float = 0.70
    aws_region: Optional[str] = None
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"


class ValidationResponse(BaseModel):
    """Response model for document field validation via Amazon Bedrock."""
    is_valid: bool
    fields: List[FieldValidation] = Field(default_factory=list)
    required_fields: List[str] = Field(default_factory=list)
    min_confidence: float = 0.70


class InvoiceSummary(BaseModel):
    """Summary of extracted invoice fields."""
    vendor: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_item_count: int = 0
    line_item_total: Optional[float] = None
    has_missing_fields: bool = False
    missing_fields: List[str] = Field(default_factory=list)


class ModerationResult(BaseModel):
    """Result of content moderation for vendor notes or memo fields."""
    is_safe: bool
    categories: Dict[str, float] = Field(default_factory=dict)
    flagged_categories: List[str] = Field(default_factory=list)
    raw_result: Optional[Dict[str, Any]] = None


class TranslationResult(BaseModel):
    """Result of translation for invoice notes or descriptions."""
    source_text: str
    source_language: Optional[str] = None
    target_text: str
    target_language: str = "en"
    confidence: float = 0.0


class ExpenseStoreResult(BaseModel):
    """Result of persisting an expense record in Pinecone vector store."""
    record_id: str
    stored: bool
    vector_id: Optional[str] = None
    index_name: str = "expense-records"
