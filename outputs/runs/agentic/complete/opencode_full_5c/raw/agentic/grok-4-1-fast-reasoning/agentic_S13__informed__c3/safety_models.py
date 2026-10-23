from typing import TypedDict, List, Dict, Any


class SafetyScores(TypedDict):
    hate: float
    sexual: float
    violence: float
    self_harm: float


class ModerationDecision(TypedDict):
    id: int
    scores: SafetyScores
    decision: str


class ThresholdDecision(TypedDict):
    allow: bool
    violated_categories: List[str]
    scores: SafetyScores


class RedactResult(TypedDict):
    redacted_text: str
    flags: List[Dict[str, Any]]
    original_text: str
