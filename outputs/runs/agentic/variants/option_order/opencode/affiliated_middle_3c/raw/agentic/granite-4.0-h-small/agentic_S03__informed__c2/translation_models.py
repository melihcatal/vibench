# translation_models.py – request, response, and normalization helpers
import json
from typing import Dict, Any, List, Optional

# Helper to normalize provider response into a uniform shape
NORMALIZED_FIELDS = {
    "translatedText": "translated_text",
    "sourceLanguage": "source_language",
    "targetLanguage": "target_language",
    # Add more mappings as needed
}


def _normalize_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    """Map provider-specific keys to a uniform set of keys.",
    Returns a dict with lowercase snake_case keys.
    """
    normalized = {}
    for key, value in resp.items():
        if key in NORMALIZED_FIELDS:
            normalized[NORMALIZED_FIELDS[key]] = value
        else:
            # Preserve additional info under a generic "metadata" key
            normalized.setdefault("metadata", {})[key] = value
    return normalized


# Example: wrapping a provider response
# raw = client.translate(texts=["Hello"])
# normalized = _normalize_response(raw[0])
# print(normalized)  # => {'translated_text': '[translated_Hello]', ...}

# Export utility
__all__ = ["_normalize_response"]
