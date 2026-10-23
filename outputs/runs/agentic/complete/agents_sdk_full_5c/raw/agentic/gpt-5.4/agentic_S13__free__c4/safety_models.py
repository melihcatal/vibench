from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    category: str
    score: float
    blocked: bool = False


@dataclass
class ModerationDecision:
    text: str
    allowed: bool
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    provider: str = "azure_ai_content_safety"
    redacted_text: Optional[str] = None
    reason: Optional[str] = None

    def category_map(self) -> Dict[str, float]:
        return {item.category: item.score for item in self.categories}


@dataclass
class BatchModerationResult:
    decisions: List[ModerationDecision]
    provider: str = "azure_ai_content_safety"


@dataclass
class ThresholdConfig:
    sexual: float = 4.0
    violence: float = 4.0
    hate: float = 4.0
    self_harm: float = 4.0

    def as_dict(self) -> Dict[str, float]:
        return {
            "sexual": self.sexual,
            "violence": self.violence,
            "hate": self.hate,
            "self_harm": self.self_harm,
        }


def normalize_azure_categories(categories_analysis: List[Dict[str, Any]]) -> List[SafetyCategoryScore]:
    normalized: List[SafetyCategoryScore] = []
    for item in categories_analysis or []:
        normalized.append(
            SafetyCategoryScore(
                category=str(item.get("category", "")).lower(),
                score=float(item.get("severity", 0)),
                blocked=bool(item.get("filtered", False)),
            )
        )
    return normalized


def extract_masked_text(response: Dict[str, Any]) -> Optional[str]:
    return response.get("redactedText") or response.get("maskedText")
