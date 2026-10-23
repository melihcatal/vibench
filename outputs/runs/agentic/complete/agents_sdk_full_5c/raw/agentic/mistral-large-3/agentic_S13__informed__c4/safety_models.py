"""
Local request, response, and normalization helpers for Text Content Safety.
"""
from typing import List, Dict, Optional, TypedDict
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    SELF_HARM = "self_harm"
    HARASSMENT = "harassment"
    DANGEROUS = "dangerous"


class SafetyDecision(TypedDict):
    category: SafetyCategory
    score: float
    flagged: bool
    threshold: Optional[float]


class TextModerationRequest:
    def __init__(self, text: str, categories: Optional[List[SafetyCategory]] = None):
        self.text = text
        self.categories = categories or list(SafetyCategory)


class TextModerationResponse:
    def __init__(self, decisions: List[SafetyDecision], raw_response: Optional[Dict] = None):
        self.decisions = decisions
        self.raw_response = raw_response

    def is_flagged(self) -> bool:
        return any(decision["flagged"] for decision in self.decisions)


def normalize_azure_scores(raw_scores: Dict) -> List[SafetyDecision]:
    """Normalize Azure AI Content Safety raw scores to standard decisions."""
    decisions = []
    for category in SafetyCategory:
        score = raw_scores.get(f"{category.value}_score", 0.0)
        decisions.append({
            "category": category,
            "score": score,
            "flagged": score >= 0.5,  # Azure default threshold
            "threshold": 0.5,
        })
    return decisions


def normalize_perspective_scores(raw_scores: Dict) -> List[SafetyDecision]:
    """Normalize Perspective API raw scores to standard decisions."""
    decisions = []
    for attribute, score_data in raw_scores.get("attributeScores", {}).items():
        category = {
            "TOXICITY": SafetyCategory.HARASSMENT,
            "SEVERE_TOXICITY": SafetyCategory.HATE,
            "IDENTITY_ATTACK": SafetyCategory.HATE,
            "INSULT": SafetyCategory.HARASSMENT,
            "PROFANITY": SafetyCategory.SEXUAL,
            "THREAT": SafetyCategory.VIOLENCE,
            "SEXUALLY_EXPLICIT": SafetyCategory.SEXUAL,
        }.get(attribute, None)
        if category:
            decisions.append({
                "category": category,
                "score": score_data["summaryScore"]["value"],
                "flagged": score_data["summaryScore"]["value"] >= 0.7,
                "threshold": 0.7,
            })
    return decisions