# [HELPER] document_models.py
"""Define local request, response, and normalization helpers for OCR and Layout Extraction."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List


# Request models
@dataclass
class OCRRequest:
    image_path: str
    language: str = "en"


@dataclass
class LayoutRequest:
    image_path: str
    page_index: int = 0


@dataclass
class KVRequest:
    image_path: str
    max_pairs: int = 50


@dataclass
class TableRequest:
    image_path: str
    max_cells: int = 500


# Normalized response models with provider field for traceability
class BaseResponse:
    def __init__(self, provider: str):
        self.provider = provider


@dataclass
class OCRResponse(BaseResponse):
    text: str


@dataclass
class LayoutResponse(BaseResponse):
    elements: List[Dict[str, Any]]  # dicts representing blocks, lines, tables, etc.


@dataclass
class KVResponse(BaseResponse):
    key_values: Dict[str, str]


@dataclass
class TableResponse(BaseResponse):
    tables: List[Dict[str, Any]]  # each table includes its own rows/cols data


# Example normalization utility (extend as needed)
def normalize_ocr_response(raw: Any) -> OCRResponse:
    """Convert provider-specific OCR result to our normalized response."""
    # Placeholder: real code would map fields from raw SDK response to OCRResponse
    return OCRResponse(text=str(raw), provider="placeholder-OCR")


# Export the model classes for use in integration steps
__all__ = [
    "OCRRequest",
    "LayoutRequest",
    "KVRequest",
    "TableRequest",
    "OCRResponse",
    "LayoutResponse",
    "KVResponse",
    "TableResponse",
]
