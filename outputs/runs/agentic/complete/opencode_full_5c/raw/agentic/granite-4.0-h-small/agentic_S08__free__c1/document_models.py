# [HELPER] document_models.py

# Local request, response, and helper definitions for Structured Document Extraction
from pydantic import BaseModel, Field, validator
import re
from typing import List, Optional


class ExtractionResult(BaseModel):
    """Holds raw extraction data from an OCR service."""

    document_type: str = Field(..., description="Invoice or receipt")
    raw: dict = Field(..., description="Raw output from document client")
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: Optional[List[str]] = None
    merchant: Optional[str] = None
    tax: Optional[float] = None
    items: Optional[List[str]] = None
    confidence: float = Field(..., description="Overall confidence score, 0-1")

    @validator("confidence")
    def validate_confidence(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("confidence must be between 0 and 1")
        return v


class NormalizedExpense(BaseModel):
    """Standardized expense record used downstream."""

    vendor: str
    date: str
    total: float
    items: List[str]
