# [HELPER] document_models.py
"""Local request, response, and normalization helpers for OCR and layout extraction"""

from __future__ import annotations
from typing import Dict, List, Any, Union


# Normalized request model for OCR operations
class OCRRequest:
    def __init__(
        self,
        image_bytes: bytes,
        pages: List[int] = None,
        feature_type: str = "FORMS",
    ) -> None:
        self.image_bytes = image_bytes
        self.pages = pages or []
        self.feature_type = feature_type  # e.g. "FORMS", "TABLES"

    def to_provider_payload(self) -> Dict[str, Any]:
        payload = {"Document": {"Bytes": self.image_bytes}}
        if self.pages:
            payload["Pages"] = self.pages
        if self.feature_type:
            payload["FeatureTypes"] = [self.feature_type]
        return payload


# Normalized response models (provider-agnostic)
class OCRResponse:
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw

    @property
    def blocks(self) -> List[Dict[str, Any]]:
        return self.raw.get("Blocks", [])

    @property
    def text(self) -> str:
        """Simple concatenation of all text blocks"""
        texts = [block["Text"] for block in self.blocks if block["Confidence"] > 70]
        return " ".join(texts)


# Helper for layout extraction
class LayoutResponse(OCRResponse):
    """Layout response already includes blocks/lines/tables"""


# Helper for tables extraction
TableCell = Dict[str, Any]


class TableResponse:
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw

    @property
    def tables(self) -> List[Dict[str, Any]]:
        return self.raw.get("Tables", [])

    @property
    def cells(self) -> List[TableCell]:
        cells = []
        for tbl in self.tables:
            cells.extend(tbl.get("TableCells", []))
        return cells


# Helper for key-value extraction
KeyValue = Dict[str, Any]


class KeyValueResponse:
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw

    @property
    def key_values(self) -> List[KeyValue]:
        return self.raw.get("Blocks", [])


# Example normalization utility


def normalize_response(provider_name: str, raw: Dict[str, Any]) -> Any:
    """Convert provider-specific raw payload to our generic models"""
    if provider_name == "textract":
        if "Blocks" in raw:
            return OCRResponse(raw)
        if "Tables" in raw:
            return TableResponse(raw)
        if "Blocks" in raw and any(
            b.get("Type") == "KEY_VALUE_SET" for b in raw["Blocks"]
        ):
            return KeyValueResponse(raw)
    raise ValueError(f"Unknown provider or response shape: {provider_name}")


if __name__ == "__main__":
    # Simple test with dummy data
    dummy = {"Blocks": []}
    print("Normalized OCR response:", normalize_response("textract", dummy))
