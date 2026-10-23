from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


@dataclass
class SafetyScore:
    category: SafetyCategory
    severity: int
    threshold: int = 2

    @property
    def exceeds_threshold(self) -> bool:
        return self.severity >= self.threshold

    @property
    def is_safe(self) -> bool:
        return self.severity < self.threshold


@dataclass
class ModerationRequest:
    text: str
    categories: Optional[List[SafetyCategory]] = None
    custom_thresholds: Optional[Dict[SafetyCategory, int]] = None

    def to_azure_request(self):
        from azure.ai.contentsafety.models import AnalyzeTextOptions

        return AnalyzeTextOptions(text=self.text)


@dataclass
class ModerationResponse:
    text: str
    scores: List[SafetyScore]
    overall_decision: str
    provider: str = "azure_content_safety"

    @classmethod
    def from_azure_response(cls, text: str, azure_response):
        scores = []
        for category_result in azure_response.categories_analysis:
            category = SafetyCategory(category_result.category.value)
            score = SafetyScore(category=category, severity=category_result.severity)
            scores.append(score)

        overall_decision = (
            "BLOCK" if any(score.exceeds_threshold for score in scores) else "ALLOW"
        )

        return cls(text=text, scores=scores, overall_decision=overall_decision)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "scores": [
                {
                    "category": score.category.value,
                    "severity": score.severity,
                    "exceeds_threshold": score.exceeds_threshold,
                }
                for score in self.scores
            ],
            "overall_decision": self.overall_decision,
            "provider": self.provider,
        }


@dataclass
class BatchModerationResult:
    results: List[ModerationResponse]

    def get_blocked_count(self) -> int:
        return sum(1 for result in self.results if result.overall_decision == "BLOCK")

    def get_allowed_count(self) -> int:
        return sum(1 for result in self.results if result.overall_decision == "ALLOW")
