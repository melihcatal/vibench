import json
from typing import Any, Dict, List, Optional

# -------------------------------------------------
# HELPER: document_models.py
# Defines request, response, and normalization helpers for OCR and layout tasks
# -------------------------------------------------

class OcrRequest:
    """Represents a request payload for OCR/layout extraction.","
    def __init__(self, image_bytes: bytes, feature_types: Optional[List[str]] = None):
        self.image_bytes = image_bytes
        self.feature_types = feature_types or []

    @property
    def payload(self) -> Dict[str, Any]:
        """Builds the JSON‑serializable payload for the provider API.","
        payload = {"Document": {"Bytes": self.image_bytes}}
        if self.feature_types:
            payload["FeatureTypes"] = self.feature_types
        return payload

class OcrResponse:
    """Normalizes raw provider response into a consistent internal model.","
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw

    @property
    def lines(self) -> List[str]:
        """All extracted text lines.","
        return [block["Text"] for block in self.raw.get("Blocks", []) if block.get("BlockType") == "LINE"]

    @property
    def key_values(self) -> Dict[str, str]:
        """Key‑value pairs from form‑like documents.","
        kv = {}
        for block in self.raw.get("Blocks", []):
            if block.get("BlockType") != "KEY_VALUE_SET":
                continue
            key = next((b["Text"] for b in block.get("Relationships", []) if b["Type"] == "KEY"), None)
            value = next((b["Text"] for b in block.get("Relationships", []) if b["Type"] == "VALUE"), None)
            if key and value:
                kv[key] = value
        return kv

    @property
    def tables(self) -> List[Dict[str, Any]]:
        """Tables as list of dicts, each dict contains its cells.","
        tables = []
        for block in self.raw.get("Blocks", []):
            if block.get("BlockType") != "TABLE":
                continue
            cells = []
            for field in block.get("Relationships", []):
                if field["Type"] == "CHILD":
                    for child_id in field["Ids"]:
                        child = next(
                            (b for b in self.raw.get("Blocks", []) if b.get('Id') == child_id), None
                        )
                        if child and child.get('BlockType') == "CELL":
                            cells.append(child)
            tables.append({"cells": cells})
        return tables

    @property
    def layout_blocks(self) -> List[Dict[str, Any]]:
        """All layout blocks (LINES, WORDS, TABLES, FORM_FIELDS) in raw form.","
        return self.raw.get("Blocks", [])

# Normalization utility – converts provider payload to OcrResponse
normalize_response = OcrResponse

# Simple configuration helper for provider API endpoint
provider_endpoint = os.getenv("AWS_Textract_URL", "https://textract.us-east-1.amazonaws.com")
