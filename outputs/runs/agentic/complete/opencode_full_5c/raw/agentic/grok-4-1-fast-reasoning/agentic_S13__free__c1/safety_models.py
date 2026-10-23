from typing import Dict, List, Any, TypedDict


class ModerationResultDict(TypedDict):
    flagged: bool
    scores: Dict[str, float]
    violated_categories: List[str]


class RedactionResultDict(TypedDict):
    redacted_text: str
    spans: List[Dict[str, Any]]


class SafetyDecisionDict(TypedDict):
    safe: bool
    scores: Dict[str, float]
