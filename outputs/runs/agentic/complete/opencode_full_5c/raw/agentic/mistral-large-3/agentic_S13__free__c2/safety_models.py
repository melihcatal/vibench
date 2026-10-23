from typing import Dict, List, Optional, TypedDict
from enum import Enum


class SafetyCategory(Enum):
    HATE_SPEECH = "HATE_SPEECH"
    SEXUALLY_EXPLICIT = "SEXUALLY_EXPLICIT"
    DANGEROUS_CONTENT = "DANGEROUS_CONTENT"
    HARASSMENT = "HARASSMENT"


class ModerationRequest(TypedDict):
    text: str
    threshold_overrides: Optional[Dict[SafetyCategory, float]]


class ModerationResponse(TypedDict):
    allowed: bool
    categories: List[Dict[str, float]]
    language: Optional[str]


class RedactionResponse(TypedDict):
    redacted_text: str
    unsafe_spans: List[Dict[str, int]]
    categories: List[Dict[str, float]]


def normalize_category_name(category: str) -> SafetyCategory:
    category_map = {
        "hate_speech": SafetyCategory.HATE_SPEECH,
        "hate": SafetyCategory.HATE_SPEECH,
        "sexually_explicit": SafetyCategory.SEXUALLY_EXPLICIT,
        "sexual": SafetyCategory.SEXUALLY_EXPLICIT,
        "dangerous": SafetyCategory.DANGEROUS_CONTENT,
        "dangerous_content": SafetyCategory.DANGEROUS_CONTENT,
        "harassment": SafetyCategory.HARASSMENT,
    }
    return category_map.get(category.lower(), SafetyCategory.HATE_SPEECH)
