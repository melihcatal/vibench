from typing import Dict, List, Optional, TypedDict
from enum import Enum


class ModerationCategory(Enum):
    HATE_SPEECH = "hate_speech"
    DANGEROUS_CONTENT = "dangerous_content"
    HARASSMENT = "harassment"
    SEXUALLY_EXPLICIT = "sexually_explicit"


class ModerationScores(TypedDict):
    hate_speech: float
    dangerous_content: float
    harassment: float
    sexually_explicit: float


class ModerationResult(TypedDict):
    moderation_scores: ModerationScores
    language: str
    is_allowed: bool
    flagged_categories: List[ModerationCategory]


class RedactionResult(TypedDict):
    redacted_text: str
    unsafe_spans: List[Dict[str, int]]
    flagged_categories: List[ModerationCategory]


def normalize_moderation_result(
    moderation_data: Dict, thresholds: Dict[ModerationCategory, float]
) -> ModerationResult:
    moderation_scores = moderation_data["moderation_scores"]
    flagged_categories = []

    for category, threshold in thresholds.items():
        if moderation_scores[category.value] >= threshold:
            flagged_categories.append(category)

    return {
        "moderation_scores": moderation_scores,
        "language": moderation_data.get("language", "unknown"),
        "is_allowed": len(flagged_categories) == 0,
        "flagged_categories": flagged_categories,
    }
