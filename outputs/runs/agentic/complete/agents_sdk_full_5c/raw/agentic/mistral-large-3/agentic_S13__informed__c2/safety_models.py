"""
Local request, response, and normalization helpers for Text Content Safety.
"""
from typing import Dict, List, Optional, TypedDict


class SafetyCategory(TypedDict):
    category: str
    score: float
    label: Optional[str]


class SafetyResponse(TypedDict):
    text: str
    categories: List[SafetyCategory]
    flagged: bool
    provider: str


class SafetyRequest(TypedDict):
    text: str
    categories: Optional[List[str]]
    threshold: Optional[float]


def normalize_azure_response(data: Dict, text: str) -> SafetyResponse:
    """Normalize Azure AI Content Safety response to local model."""
    categories = []
    for result in data.get("categoriesAnalysis", []):
        categories.append({
            "category": result["category"],
            "score": result["severity"] / 6.0,  # Normalize 0-6 to 0-1
            "label": "flagged" if result["severity"] > 0 else "passed"
        })
    return {
        "text": text,
        "categories": categories,
        "flagged": any(c["score"] > 0 for c in categories),
        "provider": "azure_content_safety"
    }


def normalize_perspective_response(data: Dict, text: str) -> SafetyResponse:
    """Normalize Perspective API response to local model."""
    categories = []
    for attribute, scores in data.get("attributeScores", {}).items():
        categories.append({
            "category": attribute,
            "score": scores["summaryScore"]["value"],
            "label": "flagged" if scores["summaryScore"]["value"] > 0.5 else "passed"
        })
    return {
        "text": text,
        "categories": categories,
        "flagged": any(c["score"] > 0.5 for c in categories),
        "provider": "perspective_api"
    }


def normalize_watsonx_response(data: Dict, text: str) -> SafetyResponse:
    """Normalize watsonx.ai HAP detection response to local model."""
    categories = []
    for result in data.get("results", []):
        categories.append({
            "category": result["type"],
            "score": result["score"],
            "label": "flagged" if result["score"] > 0.5 else "passed"
        })
    return {
        "text": text,
        "categories": categories,
        "flagged": any(c["score"] > 0.5 for c in categories),
        "provider": "watsonx_guardrails"
    }