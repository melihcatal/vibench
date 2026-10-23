import os
from typing import TypedDict

# Minimal wrapper to hold raw document bytes & meta for OCR/layout calls

class RawDocument(TypedDict):
    """Holds raw image or PDF bytes and MIME type for processing."""
    content: bytes
    mime_type: str
    processor_id: str  # ID of the OCR/layout processor in your cloud project

# Normalized response structure shared across different extractors

class LayoutElement(TypedDict):
    """Generic layout element produced by OCR/layout processors."""
    type: str  # e.g., 'TOKEN', 'BLOCK', 'LINE', 'TABLE'"
    text: str
    bbox: list[float]  # [x0, y0, x1, y1] normalized coordinates

class KeyValue(TypedDict):
    key: LayoutElement
    value: LayoutElement

class DocumentExtraction(TypedDict):
    """Unified container for text, layout, tables, and key-value pairs."""
    text: str
    layout: list[LayoutElement]
    tables: list[list[LayoutElement]]  # list of rows, each row is list of cells (LayoutElement)
    key_values: list[KeyValue]

# Helper to create RawDocument instances

def create_raw_document(path: str, mime_type: str, processor_id: str) -> RawDocument:
    with open(path, "rb") as fp:
        return {
            "content": fp.read(),
            "mime_type": mime_type,
            "processor_id": processor_id,
        }

# Helper to convert from provider-specific responses to our DocumentExtraction
# (Implementations would subclass/override in each extractor file)

class DocumentExtractionHelper:
    @staticmethod
    def from_ai_response(ai_response):
        """Override per provider to map AI response -> DocumentExtraction."""
        raise NotImplementedError

    @staticmethod
    def normalize_layout(elements):
        normalized = []
        for elem in elements:
            normalized.append(
                {
                    "type": elem.get("type", "UNKNOWN"),
                    "text": elem.get("text", ""),
                    "bbox": elem.get(
                        "boundingPoly", []
                    )  # assume coords are normalized
                }
            )
        return normalized
