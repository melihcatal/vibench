# [HELPER] document_models.py

from typing import TypedDict, List, Dict

# ---------- Request models ----------


class OCRRequest(TypedDict):
    image_path: str
    model: str = "gpt-4o-mini"  # concrete provider identifier


class LayoutRequest(TypedDict):
    image_path: str
    model: str = "gpt-4o-mini"


class TableRequest(TypedDict):
    image_path: str
    model: str = "gpt-4o-mini"


class KeyValueRequest(TypedDict):
    image_path: str
    model: str = "gpt-4o-mini"


# ---------- Normalization helpers ----------


def normalize_ocr_response(raw: str) -> List[str]:
    """Convert raw model output into a clean list of lines."""
    return [line.strip() for line in raw.strip().splitlines() if line.strip()]


def normalize_layout_response(raw: str) -> List[Dict]:
    """Parse JSON layout output into a list of element dicts."""
    import json

    return json.loads(raw)


def normalize_table_response(raw: str) -> List[List[str]]:
    """Parse JSON table output into a 2D list of cell strings."""
    import json

    return json.loads(raw)


def normalize_key_value_response(raw: str) -> Dict[str, str]:
    """Parse JSON key‑value output into a dict."""
    import json

    return json.loads(raw)
