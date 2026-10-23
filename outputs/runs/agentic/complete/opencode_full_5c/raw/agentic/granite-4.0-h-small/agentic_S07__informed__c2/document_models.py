import json


class DocumentModels:
    """Define local request, response, and normalization helpers for OCR and Layout Extraction."""

    class OCRResponse:
        def __init__(self, raw):
            self.raw = raw
            self.text = raw.get("text", "")
            self.tables = raw.get("tables", [])
            self.entities = raw.get("entities", [])

    class LayoutResponse:
        def __init__(self, raw):
            self.raw = raw
            # Simplify to a list of block objects
            self.blocks = raw.get("blocks", [])

        def to_dict(self):
            return {"blocks": self.blocks}

    class TableResponse:
        def __init__(self, tables):
            self.tables = tables

    class KeyValuesResponse:
        def __init__(self, kv_dict):
            self.key_values = kv_dict

    @staticmethod
    def normalize_text(raw_text):
        """Basic normalization: strip whitespace, normalize newlines."""
        return " ".join(raw_text.split())

    @staticmethod
    def normalize_entities(entities):
        """Filter and return a list of dicts with id and text."""
        return [
            {"id": e.id, "text": e.text}
            for e in entities
            if e.type_ in ("LABEL_DETECTION", "TEXT_DETECTION")
        ]
