import os
from enum import Enum
from typing import List, Dict, Any, Optional


class ModerationCategory(str, Enum):
    HATE = "Hate"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"
    SELF_HARM = "SelfHarm"


class TextModerationRequest:
    def __init__(self, text: str):
        self.text = text


class TextModerationResponse:
    def __init__(
        self,
        categories_analysis: List[Dict[str, Any]],
        hates: Optional[List[Dict[str, Any]]] = None,
        sexuals: Optional[List[Dict[str, Any]]] = None,
        violences: Optional[List[Dict[str, Any]]] = None,
        self_harms: Optional[List[Dict[str, Any]]] = None,
    ):
        self.categories_analysis = categories_analysis
        self.hates = hates
        self.sexuals = sexuals
        self.violences = violences
        self.self_harms = self_harms

    def get_category_score(self, category: ModerationCategory) -> Optional[float]:
        for cat in self.categories_analysis:
            if cat.get("category") == category.value:
                return cat.get("score")
        return None

    def is_unsafe(self, category: ModerationCategory, threshold: float) -> bool:
        score = self.get_category_score(category)
        return score is not None and score >= threshold


class BatchModerationRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class BatchModerationResponse:
    def __init__(self, results: List[TextModerationResponse]):
        self.results = results


class RedactRequest:
    def __init__(self, text: str, categories_to_redact: List[ModerationCategory]):
        self.text = text
        self.categories_to_redact = categories_to_redact


class RedactResponse:
    def __init__(
        self,
        original_text: str,
        redacted_text: str,
        detected_spans: List[Dict[str, Any]],
    ):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.detected_spans = detected_spans
