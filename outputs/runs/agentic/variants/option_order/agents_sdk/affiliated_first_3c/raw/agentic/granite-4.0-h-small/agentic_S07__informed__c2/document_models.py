from typing import TypedDict

# Simple DTOs to standardize inputs/outputs across OCR/layout steps

class RawDocument(TypedDict):
    """Encapsulates a document image or PDF and the processor to use."""
    content: bytes
    mime_type: str
    processor_id: str

class DocumentExtraction(TypedDict):
    """Unified structure returned from every same-scenario extractor."""
    text: str
    layout: list[dict]
    tables: list[list[dict]]
    key_values: list[dict]

# Helper functions (can be expanded in real code)

def is_blank(text: str) -> bool:
    """Very simple blank check for post‑processing."""
    return not text.strip()

# Example of a generic normalization routine that could be reused

def standardize_bbox(bbox: list[float]) -> list[float]:
    """Ensure bbox values are within [0.0, 1.0]."""
    return [max(0.0, min(1.0, v)) for v in bbox]
