from typing import TypedDict


class ModerationResult(TypedDict):
    text: str
    decision: str  # 'safe' or 'unsafe'
    flags: list[str]
    scores: dict[str, float]


class RedactionResponse(TypedDict):
    redacted_text: str


class ThresholdConfig(TypedDict):
    category: str
    limit: float
