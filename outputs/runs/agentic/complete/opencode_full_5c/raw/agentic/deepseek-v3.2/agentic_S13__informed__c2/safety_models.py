from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass


class ModerationRequest(TypedDict):
    text: str
    categories: Optional[List[str]]
    blocklist_names: Optional[List[str]]


class ModerationResponse(TypedDict):
    text: str
    scores: Dict[str, int]
    flagged: bool
    error: Optional[str]


class BatchModerationResponse(TypedDict):
    message: str
    decision: str
    categories_flagged: List[str]
    scores: Dict[str, int]
    error: Optional[str]


class RedactionResponse(TypedDict):
    original_text: str
    redacted_text: str
    unsafe_spans: List[Dict]
    has_unsafe_content: bool
    error: Optional[str]


class ThresholdResponse(TypedDict):
    text: str
    decision: str
    exceeded_thresholds: List[Dict]
    category_scores: Dict[str, int]
    thresholds_applied: Dict[str, int]
    error: Optional[str]


@dataclass
class SafetyCategory:
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"

    @classmethod
    def all_categories(cls) -> List[str]:
        return [cls.HATE, cls.SELF_HARM, cls.SEXUAL, cls.VIOLENCE]


@dataclass
class ModerationDecision:
    ALLOW = "allow"
    BLOCK = "block"
    ERROR = "error"


def normalize_text(text: str) -> str:
    """Normalize text for moderation."""
    return text.strip()


def parse_severity_level(severity: int) -> str:
    """Parse severity level to human-readable format."""
    levels = {0: "Safe", 1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
    return levels.get(severity, f"Unknown ({severity})")


def format_moderation_result(result: Dict) -> str:
    """Format moderation result for display."""
    if "error" in result:
        return f"Error: {result['error']}"

    if result.get("flagged", False):
        scores_str = ", ".join(
            [f"{cat}: {score}" for cat, score in result.get("scores", {}).items()]
        )
        return f"FLAGGED - Scores: {scores_str}"
    else:
        return "SAFE"
