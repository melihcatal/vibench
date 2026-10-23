from typing import TypedDict, List


class SafetyScore(TypedDict):
    category: str
    score: float


class SafetyResult(TypedDict):
    input_text: str
    blocked: bool
    scores: List[SafetyScore]
    flagged_categories: List[str]
