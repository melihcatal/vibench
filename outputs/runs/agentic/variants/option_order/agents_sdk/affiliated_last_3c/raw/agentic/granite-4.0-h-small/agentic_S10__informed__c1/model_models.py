import json
from typing import Any, Dict

def normalize_text(raw: str) -> str:
    """Strip whitespace and ensure non‑empty string."""
    return raw.strip() or ""

def normalize_json(raw: str) -> Dict[str, Any]:
    """Parse JSON text, raise ValueError if invalid."""
    if not raw:
        raise ValueError("Empty JSON string")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}")

# Additional utility functions (e.g., for result translation, embeddings) can be added here.
