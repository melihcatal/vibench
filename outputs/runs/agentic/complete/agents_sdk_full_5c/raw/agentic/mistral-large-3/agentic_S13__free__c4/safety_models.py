"""
Local request, response, and normalization helpers for Text Content Safety.
Uses Google Cloud's Perspective API models for content safety categorization.
"""
from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass


class PerspectiveRequest(TypedDict):
    comment: Dict[str, str]
    requestedAttributes: Dict[str, Dict]
    languages: Optional[List[str]]
    doNotStore: Optional[bool]


@dataclass
class SafetyCategoryScore:
    category: str
    score: float


@dataclass
class TextModerationResult:
    text: str
    scores: List[SafetyCategoryScore]
    client_token: Optional[str] = None


@dataclass
class TextRedactionResult:
    original_text: str
    redacted_text: str
    unsafe_spans: List[Dict[str, int]]
    client_token: Optional[str] = None


def build_perspective_request(text: str, categories: List[str]) -> PerspectiveRequest:
    """Build a Perspective API request for the given text and categories."""
    return {
        "comment": {"text": text},
        "requestedAttributes": {cat: {} for cat in categories},
        "languages": ["en"],
        "doNotStore": True
    }


def normalize_perspective_response(response: Dict, text: str) -> TextModerationResult:
    """Normalize Perspective API response into a structured result."""
    scores = []
    for category, attribute in response.get("attributeScores", {}).items():
        score = attribute.get("summaryScore", {}).get("value", 0.0)
        scores.append(SafetyCategoryScore(category=category, score=score))
    return TextModerationResult(text=text, scores=scores)