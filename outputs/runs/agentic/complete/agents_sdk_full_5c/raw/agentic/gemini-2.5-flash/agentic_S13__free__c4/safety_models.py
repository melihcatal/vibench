# safety_models.py
# This file defines local request, response, and normalization helpers for Text Content Safety.

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ModerationCategoryScore:
    category: str
    score: float
    severity: str = None
    blocked: bool = False

@dataclass
class ModerationResult:
    text: str
    flagged: bool
    scores: List[ModerationCategoryScore] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    redaction_applied: bool

@dataclass
class ThresholdConfiguration:
    thresholds: Dict[str, float]
    default_block_if_any_exceeds: bool = True

