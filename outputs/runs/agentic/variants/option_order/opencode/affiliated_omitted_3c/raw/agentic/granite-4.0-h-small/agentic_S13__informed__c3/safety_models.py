# safety_models.py
"""Local request, response, and normalization helpers for Text Content Safety"""

from typing import List, Dict, Any

# Example data structures for a concrete provider (Azure AI Content Safety)


def build_api_request(text: str, categories: List[str]) -> Dict[str, Any]:
    """Build request dictionary expected by the safety client."""
    return {
        "content": text,
        "categories": categories,
    }


ResponseModel = Dict[str, Any]


def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize response to a consistent shape across providers."""
    # Assuming raw follows Azure's format
    unsafe_spans = raw.get("unsafe_spans", [])
    category_scores = raw.get("category_scores", {})
    return {
        "unsafe_spans": unsafe_spans,
        "category_scores": category_scores,
    }
