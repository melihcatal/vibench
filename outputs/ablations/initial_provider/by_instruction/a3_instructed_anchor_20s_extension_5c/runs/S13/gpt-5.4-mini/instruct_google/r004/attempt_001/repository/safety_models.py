from dataclasses import dataclass, field
from typing import Any, Dict, List


def normalize_text(text: str) -> str:
    return (text or "").strip()


@dataclass
class SafetyDecision:
    allowed: bool
    category_scores: Dict[str, float] = field(default_factory=dict)
    rationale: str = ""


@dataclass
class BatchSafetyDecision:
    decisions: List[SafetyDecision]


@dataclass
class RedactionResult:
    text: str
    spans: List[Dict[str, Any]] = field(default_factory=list)
