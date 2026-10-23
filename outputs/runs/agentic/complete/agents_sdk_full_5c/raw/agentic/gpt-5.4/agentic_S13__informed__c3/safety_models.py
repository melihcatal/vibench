from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    name: str
    score: float
    blocked: bool = False


@dataclass
class ModerationResult:
    text: str
    provider: str
    model: Optional[str] = None
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    overall_score: float = 0.0
    block: bool = False
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "provider": self.provider,
            "model": self.model,
            "categories": [
                {"name": c.name, "score": c.score, "blocked": c.blocked}
                for c in self.categories
            ],
            "overall_score": self.overall_score,
            "block": self.block,
            "raw_response": self.raw_response,
        }


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]

    def to_dict(self) -> Dict[str, Any]:
        return {"results": [item.to_dict() for item in self.results]}


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: List[Dict[str, Any]]
    provider: str
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "redacted_text": self.redacted_text,
            "flagged_spans": self.flagged_spans,
            "provider": self.provider,
            "raw_response": self.raw_response,
        }


def normalize_azure_categories(response_json: Dict[str, Any]) -> List[SafetyCategoryScore]:
    categories = []
    for item in response_json.get("categoriesAnalysis", []):
        categories.append(
            SafetyCategoryScore(
                name=str(item.get("category", "unknown")).lower(),
                score=float(item.get("severity", 0)),
                blocked=bool(item.get("filtered", False)),
            )
        )
    return categories


def max_score(categories: List[SafetyCategoryScore]) -> float:
    return max((c.score for c in categories), default=0.0)
