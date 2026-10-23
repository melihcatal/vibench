import os
from typing import TypedDict, List, Dict

# Normalized models for OCR responses (common fields across providers)

class BoundingBox(TypedDict):
    vertices: List[Dict[str, int]]

class OCRResult(TypedDict):
    text: str
    language: str
    blocks: List[Dict[str, str]]  # Each block may contain lines, paragraphs, bounding box

class LayoutElement(TypedDict):
    type: str  # e.g., 'paragraph', 'line', 'table'
    text: str
    bounding_box: BoundingBox | None


class KeyValues(TypedDict):
    keys: List[str]
    values: List[str]

# Example normalization function (could be expanded per provider)
def normalize_layout(elements: List[LayoutElement]) -> List[Dict[str, str]]:
    normalized = []
    for el in elements:
        normalized.append({"type": el["type"], "text": el["text"]})
    return normalized
