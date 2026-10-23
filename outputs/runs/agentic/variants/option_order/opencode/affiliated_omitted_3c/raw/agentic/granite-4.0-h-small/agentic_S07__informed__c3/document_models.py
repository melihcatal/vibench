# HELPER document_models.py

from typing import Any, Dict, List


# Generic response shape for OCR/layout extraction
class OCRResponse:
    def __init__(self, text: str = ""):
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text}


# Layout element model (minimal for illustration)
LayoutElement = Dict[str, Any]


class LayoutResponse:
    def __init__(self, elements: List[LayoutElement]):
        self.elements = elements

    def to_dict(self) -> Dict[str, Any]:
        return {"layout": self.elements}


# Table cell model (minimal)
TableCell = Dict[str, Any]

Table = Dict[str, Any]


class TableResponse:
    def __init__(self, tables: List[Table]):
        self.tables = tables

    def to_dict(self) -> Dict[str, Any]:
        return {"tables": self.tables}


# Key-value pair extraction model
KVPair = Dict[str, Dict[str, Any]]


class KeyValueResponse:
    def __init__(self, key_values: List[KVPair], other_entities: List[Dict[str, Any]]):
        self.key_values = key_values
        self.other_entities = other_entities

    def to_dict(self) -> Dict[str, Any]:
        return {"key_values": self.key_values, "other_entities": self.other_entities}


# Normalization helper – converts provider-specific dicts to our internal models
params = {
    "google_documentai": lambda resp: LayoutResponse(
        [
            {
                "type": e.type,
                "text": e.text,
                "bounding_poly": e.bounding_poly.vertices,
                "confidence": e.confidence,
            }
            for page in resp.document.pages
            for e in page.layout
        ]
    )
}


def normalize_response(provider: str, raw: Any) -> Any:
    """Convert provider-specific raw payload to our internal model."""
    if provider in params:
        return params[provider](raw)
    # Default: assume raw is already plain text
    return OCRResponse(raw)
