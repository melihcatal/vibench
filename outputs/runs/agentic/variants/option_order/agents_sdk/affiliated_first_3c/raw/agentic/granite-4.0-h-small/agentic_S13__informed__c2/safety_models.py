# [HELPER] safety_models.py

from typing import NamedTuple, Dict, List

# Uniform representation of a moderation result used across our service files.

class UnsafeSpan(NamedTuple):
    start: int
    end: int
    category: str
    score: float

class TextModerationResult(NamedTuple):
    decision: str               # e.g., 'safe', 'unsafe', 'error'
    detailed: Dict[str, float]  # scores per category (hate, selfHarm, sexual, violence)
    thresholds: Dict[str, float]
    error: str = ''
    details: Dict = {}
