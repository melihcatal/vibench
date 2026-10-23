import json
from typing import TypedDict, List, Optional

# Request & Response models for generic extraction workflow

class ExtractionRequest(TypedDict):
    document: bytes
    provider: str

    # Optional metadata for validation
    expected_fields: Optional[List[str]] = None

class ExtractionResponse(TypedDict):
    vendor: Optional[str]
    date: Optional[str]
    total: Optional[float]
    items: Optional[List[dict]]

    # Confidence scores (0.0 to 1.0)
    confidence: Optional[dict]

class NormalizedExpense(TypedDict):
    vendor: str
    date: str
    total: float
    items: List[dict]
    confidence: dict

class ValidationStatus(TypedDict):
    valid: bool
    message: Optional[str]

class ModeratorResult(TypedDict):
    safe: bool
    flagged_categories: Optional[List[str]]

class TranslationResult(TypedDict):
    translated_text: str
    detected_source_language: Optional[str]

__all__ = ["ExtractionRequest", "ExtractionResponse", "NormalizedExpense", "ValidationStatus", "ModeratorResult", "TranslationResult"]
